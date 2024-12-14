from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
import poseidon

P = poseidon.parameters.prime_254
CIRCOM_P = int(21888242871839275222246405745257275088548364400416034343698204186575808495617)
CIRCOM_HASH_OUTPUT = int(7853200120776062878684798364095072458815029376092732009249414926327459813530)

def task(h_type, alpha):
    poseidon_new = poseidon.OptimizedPoseidon(
        h_type=h_type,
        p=P, 
        security_level=0, 
        alpha=alpha,
        input_rate=0,
        t=3,
        full_round=8,
        partial_round=19,
        mds_matrix=poseidon.matrix_circom,
        rc_list=poseidon.round_constants_circom,
    )

    input_vec = [1, 2]
    poseidon_output = poseidon_new.run_hash(input_vec)
    print(input_vec)
    return int(poseidon_output)

def main():
    if P != CIRCOM_P:
        raise Exception("prime field modulus does not match")

    with ProcessPoolExecutor(max_workers=16) as executor:
        tasks = [
            executor.submit(task, h_type, alpha) for h_type, alpha in product([poseidon.HashType.CONSTINPUTLEN, poseidon.HashType.MERKLETREE], range(1, 20))
        ]
        for future in as_completed(tasks):
            try:
                result = future.result()
            except Exception as exc:
                print(f"exception: {exc}")
            else:
                print(f"result: {result}")
                if result == CIRCOM_HASH_OUTPUT:
                    print("WIN WIN WIN")
                    break


if __name__ == "__main__":
    main()
