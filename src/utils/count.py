from schemas import CountWithPaginationIn


class Count:

    @staticmethod
    def pagination_count(page: int = None, skip: int = None, limit: int = None, count: int = None):
        if page is not None:
            skip = (page - 1) * limit

        if skip is not None:
            page = (skip // limit) + 1

        results = CountWithPaginationIn(
            counts=count,
            page=page,
            skip=skip,
            limit=limit,
        )

        return results
