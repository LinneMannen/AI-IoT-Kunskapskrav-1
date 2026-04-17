import numpy as np
import polars as pl
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval


class VectorStore:
    """
    Hanterar lagring och sökning av embeddings.
    
    Läser embeddings från en parquet-fil och möjliggör likhetssökning
    (cosine similarity) för att hitta relevanta dokument.
    """

    def __init__(self, parquet_path):
        """
        Laddar embeddings från parquet och förbereder dem för sökning.
        """
        self.df = pl.read_parquet(parquet_path)

        # Skapar en matris med alla embeddings (för snabb beräkning)
        self.embedding_matrix = self._prepare_embeddings()

    def _prepare_embeddings(self):
        """
        Konverterar embeddings från dataframe till en numpy-matris.

        Behövs eftersom similarity-beräkning kräver numeriska arrayer.
        """
        embeddings_list = self.df["embedding"].to_list()

        # Hanterar fall där embeddings är sparade som strängar
        def parse(x):
            if isinstance(x, str):
                return literal_eval(x)
            return x

        embeddings_list = [parse(x) for x in embeddings_list]

        # Skapar en matris: (antal dokument x embedding-dimension)
        return np.array(embeddings_list, dtype=np.float32)

    def search(self, query_embedding, k=5):
        """
        Söker efter de k mest liknande dokumenten baserat på cosine similarity.

        Args:
            query_embedding: embedding av användarens fråga
            k (int): antal resultat att returnera

        Returns:
            DataFrame med de mest relevanta dokumenten
        """

        # Gör om query till rätt format (1 x dimension)
        query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

        # Beräknar likhet mellan query och alla dokument
        similarities = cosine_similarity(query_embedding, self.embedding_matrix)[0]

        # Hämtar index för de mest liknande dokumenten
        top_idx = np.argsort(similarities)[::-1][:k]

        # Hämtar motsvarande rader från dataframe
        results = self.df[top_idx]

        # Lägger till similarity-score
        results = results.with_columns(
            pl.Series("similarity", similarities[top_idx])
        )

            # Behåll text + similarity + allt annat utom embedding
        cols_to_return = ["text", "similarity"] + [
            col for col in results.columns
            if col not in ["text", "similarity", "embedding"]
        ]

        return results.select(cols_to_return).to_dicts()

        """
        # Returnerar endast relevanta kolumner
        return results.select([
            "text",
            "similarity",
            "course_name",
            "chapter_title",
            "lesson_title",
            "file"
        ])
        """
    