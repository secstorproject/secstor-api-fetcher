from utils.reconstructer import Reconstructer
from utils.splitter import Splitter
from utils.parameters import N, K, KEYS_TO_RECONSTRUCT


def main():
    splitter = Splitter(N, K)
    splitter.run_test()

    reconstructer = Reconstructer(N, K, KEYS_TO_RECONSTRUCT)
    reconstructer.run_test()


if __name__ == "__main__":
    main()
