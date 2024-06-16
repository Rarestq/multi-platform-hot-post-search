from .query_strategy import LatestStrategy, TopStrategy, HottestStrategy

# Factory class to get the appropriate strategy based on mode
class QueryStrategyFactory:
    @staticmethod
    def get_strategy(mode):
        if mode == 'latest':
            return LatestStrategy()
        elif mode == 'top':
            return TopStrategy()
        elif mode == 'hottest':
            return HottestStrategy()
        else:
            return HottestStrategy()  # Default to 'hottest' if mode is unrecognized
