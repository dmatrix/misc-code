import sys

if __name__ == "__main__":
   equation = sys.argv[1] if len(sys.argv)  > 1 else "y=mx+c"
   print(f"equation={equation}")
