import os
from typing import List, Tuple, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from utils import parse_pdf, parse_txt, chunk_text, get_file_extension

# Try to import local LLM options
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    LOCAL_LLM_AVAILABLE = True
except ImportError:
    LOCAL_LLM_AVAILABLE = False
    print("Warning: transformers not installed. Install with: pip install transformers torch")

class LocalLLM:
    """Free local LLM using HuggingFace transformers"""
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        if not LOCAL_LLM_AVAILABLE:
            raise ImportError("transformers library not available")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
    def __call__(self, prompt: str) -> str:
        """Generate response from prompt"""
        try:
            # Encode the input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new part (after the prompt)
            if prompt in response:
                response = response[len(prompt):].strip()
            
            return response if response else "I understand your question, but I'm having trouble generating a detailed response."
            
        except Exception as e:
            return f"I'm experiencing technical difficulties: {str(e)}"

class RAGChatbot:
    def __init__(self):
        """
        Initialize local RAG chatbot
        """
        # Use free HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.vectorstore = None
        self.docs = []
        self.doc_sources = []

    def process_files(self, files: List[Tuple[str, str]]):
        """
        files: List of (filename, file_path)
        Parses and chunks files, embeds, and stores in FAISS.
        """
        all_chunks = []
        self.doc_sources = []
        for filename, file_path in files:
            ext = get_file_extension(filename)
            if ext == '.pdf':
                text = parse_pdf(file_path)
            elif ext == '.txt':
                text = parse_txt(file_path)
            else:
                continue
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            self.doc_sources.extend([(filename, chunk) for chunk in chunks])
        if all_chunks:
            self.vectorstore = FAISS.from_texts(all_chunks, self.embeddings)
        else:
            self.vectorstore = None

    def ask(self, query: str) -> Dict[str, Any]:
        """
        Retrieve relevant chunks and generate answer with sources.
        """
        if not self.vectorstore:
            return {"answer": "No documents available.", "sources": []}
        
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        
        # Get relevant documents
        docs = retriever.invoke(query)
        
        # Create context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate answer using the local LLM only
        try:
            llm = LocalLLM()
            prompt = f"""Based on the following context, answer the question. If the answer cannot be found in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
            answer = llm(prompt)
        except Exception as e:
            answer = f"Local LLM error: {str(e)}. Please install transformers: pip install transformers torch"
        
        # Prepare sources
        sources = []
        for doc in docs:
            try:
                # Try to find the source document
                for i, (filename, chunk) in enumerate(self.doc_sources):
                    if chunk in doc.page_content or doc.page_content in chunk:
                        sources.append({"filename": filename, "snippet": chunk[:200] + "..."})
                        break
                else:
                    sources.append({"filename": "Unknown", "snippet": doc.page_content[:200] + "..."})
            except Exception:
                sources.append({"filename": "Unknown", "snippet": doc.page_content[:200] + "..."})
        
        return {"answer": answer, "sources": sources}

    def get_memory(self):
        return self.memory.load_memory_variables({})["chat_history"]

    def clear_memory(self):
        self.memory.clear() 