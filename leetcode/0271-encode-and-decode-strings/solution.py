class Solution:
    def encode(self, strs: list[str]) -> str:
        return "".join(f"{len(part)}/{part}" for part in strs)

    def decode(self, encoded: str) -> list[str]:
        decoded = []
        i = 0

        while i < len(encoded):
            slash = encoded.index("/", i)
            n = int(encoded[i:slash])
            start = slash + 1

            i = start + n
            decoded.append(encoded[start:i])

        return decoded
