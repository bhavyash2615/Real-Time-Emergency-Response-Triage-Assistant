# from scaledown import ScaleDown

# # initialize once
# sd = ScaleDown()

# def compress_context(text, target_tokens=500):
#     """
#     Compress context safely using ScaleDown.
#     If compression fails, return original text.
#     """

#     try:
#         compressed = sd(text, target_tokens=target_tokens)
#         return compressed
#     except Exception as e:
#         print("Scaledown compression failed:", e)
#         return text