try:
    # Current package for text splitters
    from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
except ImportError:
    # Backward compatibility with older LangChain versions
    from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

text = """A Norma 175 da CVM é um marco regulatório para os fundos de investimento. 
Ela estabelece regras claras sobre a estrutura e deveres dos prestadores de serviço. 
Além disso, a norma foca na transparência para o investidor final."""

# 1. Fixed-size (Character) - Corta seco a cada 50 caracteres
fixed_splitter = CharacterTextSplitter(
    separator="", 
    chunk_size=50, 
    chunk_overlap=0
)
fixed_chunks = fixed_splitter.split_text(text)

# 2. Recursive - Tenta respeitar o parágrafo ou o ponto final
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n", ".", " "]
)
recursive_chunks = recursive_splitter.split_text(text)

print("--- FIXED SIZE CHUNKS ---")
for i, chunk in enumerate(fixed_chunks):
    print(f"Chunk {i+1}: '{chunk}'")

print("\n--- RECURSIVE CHUNKS ---")
for i, chunk in enumerate(recursive_chunks):
    print(f"Chunk {i+1}: '{chunk}'")
