from typing import List, Any


class SearchTool:
    def __init__(self, index):
        self.index = index

    def search(self, query: str) -> List[Any]:
        """
        Search documentation using text search.

        Args:
            query: User search query.

        Returns:
            Top 5 matching documentation chunks.
        """
        return self.index.search(query, num_results=5)
