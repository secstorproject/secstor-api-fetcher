SPLIT_URL = "http://localhost:8080/api/v1/secret-sharing/split"
RECONSTRUCT_URL = "http://localhost:8080/api/v1/secret-sharing/reconstruct"

SPLIT_INPUT_PATH = "./timing-tests/datasets/split/"
RECONSTRUCT_INPUT_PATH = "./timing-tests/datasets/reconstruct/"

SPLIT_OUTPUT_PATH = "./timing-tests/results/split/"
SPLIT_TEMP_OUTPUT_PATH = "./timing-tests/temp/split/"
SPLIT_HEADER = ["thread", "registro", "tempo1",
                "tempo2", "tempo3", "tempo4", "tempo5"]
RECONSTRUCT_OUTPUT_PATH = "./timing-tests/results/reconstruct/"
RECONSTRUCT_TEMP_OUTPUT_PATH = "./timing-tests/temp/reconstruct/"
RECONSTRUCT_HEADER = ["thread", "registro", "número de chaves",
                      "tempo1", "tempo2", "tempo3", "tempo4", "tempo5"]

ALGORITHMS = ['shamir', 'pss', 'css', 'krawczyk', 'pvss']

N = 3

K = 2

# Número de chaves usada na reconstrução, deve ser colocado do maior pro menor, ex.: 10, 7, 5
KEYS_TO_RECONSTRUCT = [3, 2]

# Tamanho dos datasets em kB
SIZES = [1]

# Número de objetos no dataset
NUMBER_OF_OBJECTS = 100

# Número de threads por vez
THREAD_COUNT = [1]

# Tempo de espera em segundos em caso de erro na request
ERROR_SLEEP_TIME = 1
