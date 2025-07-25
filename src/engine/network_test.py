import sys
import os



from network import Network

def run_test():
    username = input("Enter your username: ")
    n = Network()
    if n.connect(username):
        print("Connection successful! You can press Ctrl+C to close this window.")
        try:
            while True: 
                pass 
        except KeyboardInterrupt:
            print("\nDisconnecting...")
    else:
        print("Connection failed.")
    
    n.disconnect()

if __name__ == "__main__":
    run_test()


#این فایل برای تست هست
# اول توی ترمینال python src/engine/network_test.py رو اجرا کنید
# بعدش ترمینال split کنید تا ترمینال قبلی بسته نشه و python src/engine/network_test.py رو اجرا کنید