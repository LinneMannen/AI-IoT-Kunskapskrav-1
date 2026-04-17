import time
import polars as pl


class EmbeddingService:
    """
    Klass för att skapa embeddings via en extern modell.

    Klassen kapslar logiken för:
    - att generera embeddings för enskild text
    - att batcha flera dokument
    - att hantera rate limits via delay

    Används som en del av RAG-pipelinen.
    """

    def __init__(self, client, types, model="gemini-embedding-001"):
        """
        Initierar embedding-tjänsten.

        Args:
            client: API-klient för embedding-modellen
            types: Konfigurationsobjekt för modellen
            model (str): Namn på embedding-modellen
        """
        self.client = client
        self.types = types
        self.model = model

    def embed(self, text, task_type="SEMANTIC_SIMILARITY"):
        """
        Skapar en embedding för en enskild text.

        Args:
            text (str): Text som ska embedas
            task_type (str): Typ av embedding (t.ex. semantic similarity)

        Returns:
            list[float]: Vektorrepresentation av texten
        """
        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=self.types.EmbedContentConfig(task_type=task_type)
        )

        # Returnerar själva embedding-vektorn
        return response.embeddings[0].values

    def embed_documents(self, documents, task_type="SEMANTIC_SIMILARITY"):
        """
        Skapar embeddings för en lista av dokument.

        Args:
            documents (list[dict]): Lista med dokument som innehåller "text"
            task_type (str): Typ av embedding

        Returns:
            list[dict]: Dokument med tillhörande embeddings och metadata
        """
        embedded_docs = []

        for doc in documents:
            embedding = self.embed(doc["text"], task_type=task_type)

            # Behåller text + metadata tillsammans med embedding
            embedded_docs.append({
                "text": doc["text"],
                "embedding": embedding,
                "metadata": doc.get("metadata", {})
            })

        return embedded_docs

    def embed_documents_with_delay(
        self,
        documents,
        batch_size=95,
        wait_seconds=65,
        task_type="SEMANTIC_SIMILARITY"
    ):
        """
        Skapar embeddings med paus mellan batcher för att hantera rate limits.

        Args:
            documents (list[dict]): Lista med dokument
            batch_size (int): Antal requests innan paus
            wait_seconds (int): Tid att vänta mellan batcher
            task_type (str): Typ av embedding

        Returns:
            list[dict]: Dokument med embeddings och metadata
        """
        embedded_docs = []

        for i, doc in enumerate(documents, start=1):
            print(f"Embedding {i}/{len(documents)}")

            embedding = self.embed(doc["text"], task_type=task_type)

            embedded_docs.append({
                "text": doc["text"],
                "embedding": embedding,
                "metadata": doc.get("metadata", {})
            })

            # Pausar efter varje batch för att undvika rate limiting
            if i % batch_size == 0 and i < len(documents):
                print(f"\nBatch klar. Väntar {wait_seconds} sekunder...\n")
                time.sleep(wait_seconds)

        return embedded_docs
    
    def to_polars_df(self, embedded_docs):
        """
        Gör om embedded_docs till en Polars DataFrame.

        Metadata plattas ut till vanliga kolumner.
        """
        return pl.DataFrame([
            {
                "text": doc["text"],
                "embedding": doc["embedding"],
                **doc.get("metadata", {})
            }
            for doc in embedded_docs
        ])

    def save_to_parquet(self, embedded_docs, output_path):
        """
        Sparar embedded_docs till parquet.
        """
        df = self.to_polars_df(embedded_docs)
        df.write_parquet(output_path)
        print(f"Sparat till {output_path}")