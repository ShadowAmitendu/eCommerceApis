"""
E-Commerce API Test Suite
Tests all API endpoints with proper authentication and error handling
Run this file after setting up your FastAPI and filling all the required endpoints
"""

import requests

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"


# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")


def print_section(message: str):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'=' * 60}")
    print(f"  {message}")
    print(f"{'=' * 60}{Colors.END}\n")


class APITester:
    def __init__(self):
        self.tokens = {}  # Store tokens for different users
        self.user_ids = {}  # Store user IDs
        self.product_ids = []  # Store created product IDs

    def test_health_check(self):
        """Test health check endpoint"""
        print_section("Testing Health Check Endpoints")

        try:
            # Test root endpoint
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print_success("Root endpoint (/) is working")
                print_info(f"Response: {response.json()}")
            else:
                print_error(f"Root endpoint failed: {response.status_code}")

            # Test health endpoint
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print_success("Health endpoint (/health) is working")
                print_info(f"Response: {response.json()}")
            else:
                print_error(f"Health endpoint failed: {response.status_code}")

        except Exception as e:
            print_error(f"Health check failed: {str(e)}")

    def test_register_users(self):
        """Test user registration"""
        print_section("Testing User Registration")

        users = [
            {
                "name": "Admin User",
                "email": "admin@test.com",
                "password": "Admin1234",
                "role": "admin"
            },
            {
                "name": "Seller User",
                "email": "seller@test.com",
                "password": "Seller1234",
                "role": "seller"
            },
            {
                "name": "Buyer User",
                "email": "buyer@test.com",
                "password": "Buyer1234",
                "role": "buyer"
            }
        ]

        for user in users:
            try:
                response = requests.post(
                    f"{BASE_URL}/auth/register",
                    json=user
                )

                if response.status_code == 201:
                    data = response.json()
                    print_success(f"Registered {user['role']}: {user['email']}")
                    print_info(f"User ID: {data['id']}")
                    self.user_ids[user['role']] = data['id']
                elif response.status_code == 400:
                    print_info(f"{user['role']} already exists: {user['email']}")
                else:
                    print_error(f"Registration failed for {user['role']}: {response.status_code}")
                    print_error(f"Response: {response.text}")

            except Exception as e:
                print_error(f"Registration error for {user['role']}: {str(e)}")

    def test_login(self):
        """Test user login"""
        print_section("Testing User Login")

        credentials = [
            {"email": "admin@test.com", "password": "Admin1234", "role": "admin"},
            {"email": "seller@test.com", "password": "Seller1234", "role": "seller"},
            {"email": "buyer@test.com", "password": "Buyer1234", "role": "buyer"}
        ]

        for cred in credentials:
            try:
                response = requests.post(
                    f"{BASE_URL}/auth/login",
                    json={"email": cred["email"], "password": cred["password"]}
                )

                if response.status_code == 200:
                    data = response.json()
                    self.tokens[cred["role"]] = data["access_token"]
                    print_success(f"Login successful for {cred['role']}")
                    print_info(f"Token: {data['access_token'][:30]}...")
                else:
                    print_error(f"Login failed for {cred['role']}: {response.status_code}")
                    print_error(f"Response: {response.text}")

            except Exception as e:
                print_error(f"Login error for {cred['role']}: {str(e)}")

    def test_invalid_login(self):
        """Test invalid login credentials"""
        print_section("Testing Invalid Login")

        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": "wrong@test.com", "password": "WrongPass123"}
            )

            if response.status_code == 401:
                print_success("Invalid login correctly rejected (401)")
            else:
                print_error(f"Unexpected response: {response.status_code}")

        except Exception as e:
            print_error(f"Invalid login test error: {str(e)}")

    def test_create_products(self):
        """Test product creation"""
        print_section("Testing Product Creation")

        products = [
            {
                "name": "Laptop",
                "description": "High-performance gaming laptop",
                "price": 1299.99,
                "stock": 10
            },
            {
                "name": "Smartphone",
                "description": "Latest smartphone with 5G",
                "price": 899.99,
                "stock": 25
            },
            {
                "name": "Headphones",
                "description": "Wireless noise-cancelling headphones",
                "price": 299.99,
                "stock": 50
            }
        ]

        if "seller" not in self.tokens:
            print_error("Seller token not available. Login first.")
            return

        headers = {"Authorization": f"Bearer {self.tokens['seller']}"}

        for product in products:
            try:
                response = requests.post(
                    f"{BASE_URL}/products/",
                    json=product,
                    headers=headers
                )

                if response.status_code == 201:
                    data = response.json()
                    self.product_ids.append(data["id"])
                    print_success(f"Created product: {product['name']}")
                    print_info(f"Product ID: {data['id']}, Price: ${data['price']}")
                else:
                    print_error(f"Product creation failed: {response.status_code}")
                    print_error(f"Response: {response.text}")

            except Exception as e:
                print_error(f"Product creation error: {str(e)}")

    def test_get_products(self):
        """Test getting all products"""
        print_section("Testing Get All Products")

        try:
            response = requests.get(f"{BASE_URL}/products/")

            if response.status_code == 200:
                products = response.json()
                print_success(f"Retrieved {len(products)} products")
                for product in products[:3]:  # Show first 3
                    print_info(f"  - {product['name']}: ${product['price']} (Stock: {product['stock']})")
            else:
                print_error(f"Get products failed: {response.status_code}")

        except Exception as e:
            print_error(f"Get products error: {str(e)}")

    def test_get_single_product(self):
        """Test getting a single product"""
        print_section("Testing Get Single Product")

        if not self.product_ids:
            print_error("No products available. Create products first.")
            return

        try:
            product_id = self.product_ids[0]
            response = requests.get(f"{BASE_URL}/products/{product_id}")

            if response.status_code == 200:
                product = response.json()
                print_success(f"Retrieved product: {product['name']}")
                print_info(f"Details: ${product['price']}, Stock: {product['stock']}")
            else:
                print_error(f"Get single product failed: {response.status_code}")

        except Exception as e:
            print_error(f"Get single product error: {str(e)}")

    def test_update_product(self):
        """Test updating a product"""
        print_section("Testing Product Update")

        if not self.product_ids or "seller" not in self.tokens:
            print_error("Prerequisites not met. Need products and seller token.")
            return

        try:
            product_id = self.product_ids[0]
            headers = {"Authorization": f"Bearer {self.tokens['seller']}"}

            update_data = {
                "price": 1199.99,
                "stock": 15
            }

            response = requests.put(
                f"{BASE_URL}/products/{product_id}",
                json=update_data,
                headers=headers
            )

            if response.status_code == 200:
                product = response.json()
                print_success(f"Updated product: {product['name']}")
                print_info(f"New price: ${product['price']}, New stock: {product['stock']}")
            else:
                print_error(f"Product update failed: {response.status_code}")
                print_error(f"Response: {response.text}")

        except Exception as e:
            print_error(f"Product update error: {str(e)}")

    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        print_section("Testing Unauthorized Access")

        try:
            # Try to create product without token
            response = requests.post(
                f"{BASE_URL}/products/",
                json={"name": "Test", "price": 10, "stock": 5}
            )

            if response.status_code == 403 or response.status_code == 401:
                print_success("Unauthorized access correctly rejected")
            else:
                print_error(f"Unexpected response: {response.status_code}")

        except Exception as e:
            print_error(f"Unauthorized access test error: {str(e)}")

    def test_buyer_cannot_create_product(self):
        """Test that buyers cannot create products"""
        print_section("Testing Role-Based Access Control")

        if "buyer" not in self.tokens:
            print_error("Buyer token not available.")
            return

        try:
            headers = {"Authorization": f"Bearer {self.tokens['buyer']}"}
            response = requests.post(
                f"{BASE_URL}/products/",
                json={
                    "name": "Unauthorized Product",
                    "price": 99.99,
                    "stock": 5
                },
                headers=headers
            )

            if response.status_code == 403:
                print_success("Buyer correctly cannot create products (403)")
            else:
                print_error(f"Unexpected response: {response.status_code}")

        except Exception as e:
            print_error(f"Role access test error: {str(e)}")

    def test_admin_endpoints(self):
        """Test admin-only endpoints"""
        print_section("Testing Admin Endpoints")

        if "admin" not in self.tokens:
            print_error("Admin token not available.")
            return

        try:
            headers = {"Authorization": f"Bearer {self.tokens['admin']}"}

            # Get all users
            response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
            if response.status_code == 200:
                users = response.json()
                print_success(f"Admin retrieved {len(users)} users")
            else:
                print_error(f"Admin get users failed: {response.status_code}")

            # Get all products (including inactive)
            response = requests.get(
                f"{BASE_URL}/admin/products/all",
                headers=headers,
                params={"include_inactive": True}
            )
            if response.status_code == 200:
                products = response.json()
                print_success(f"Admin retrieved {len(products)} products")
            else:
                print_error(f"Admin get products failed: {response.status_code}")

        except Exception as e:
            print_error(f"Admin endpoints test error: {str(e)}")

    def test_search_products(self):
        """Test product search"""
        print_section("Testing Product Search")

        try:
            response = requests.get(
                f"{BASE_URL}/products/",
                params={"search": "Laptop"}
            )

            if response.status_code == 200:
                products = response.json()
                print_success(f"Search found {len(products)} products")
                for product in products:
                    print_info(f"  - {product['name']}")
            else:
                print_error(f"Search failed: {response.status_code}")

        except Exception as e:
            print_error(f"Search error: {str(e)}")

    def test_password_reset_flow(self):
        """Test password reset functionality"""
        print_section("Testing Password Reset Flow")

        try:
            # Request password reset
            response = requests.post(
                f"{BASE_URL}/auth/forgot-password",
                json={"email": "buyer@test.com"}
            )

            if response.status_code == 200:
                data = response.json()
                print_success("Password reset token generated")

                if "reset_token" in data and data["reset_token"]:
                    token = data["reset_token"]
                    print_info(f"Reset token: {token[:30]}...")

                    # Test reset password
                    response = requests.post(
                        f"{BASE_URL}/auth/reset-password",
                        json={
                            "token": token,
                            "new_password": "NewBuyer1234"
                        }
                    )

                    if response.status_code == 200:
                        print_success("Password successfully reset")

                        # Try logging in with new password
                        response = requests.post(
                            f"{BASE_URL}/auth/login",
                            json={"email": "buyer@test.com", "password": "NewBuyer1234"}
                        )

                        if response.status_code == 200:
                            print_success("Login successful with new password")
                        else:
                            print_error("Login failed with new password")
                    else:
                        print_error(f"Password reset failed: {response.status_code}")
                else:
                    print_info("Reset token not returned (production mode)")
            else:
                print_error(f"Forgot password failed: {response.status_code}")

        except Exception as e:
            print_error(f"Password reset test error: {str(e)}")

    def run_all_tests(self):
        """Run all tests in sequence"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║         E-COMMERCE API TEST SUITE                          ║")
        print("║         Testing all endpoints                              ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        # Run tests in order
        self.test_health_check()
        self.test_register_users()
        self.test_login()
        self.test_invalid_login()
        self.test_create_products()
        self.test_get_products()
        self.test_get_single_product()
        self.test_search_products()
        self.test_update_product()
        self.test_unauthorized_access()
        self.test_buyer_cannot_create_product()
        self.test_admin_endpoints()
        self.test_password_reset_flow()

        # Summary
        print_section("Test Suite Complete")
        print_success("All tests have been executed!")
        print_info("Check the output above for any failures")
        print_info(f"\nAPI Documentation: {BASE_URL}/docs")
        print_info(f"Health Check: {BASE_URL}/health")


def main():
    """Main entry point"""
    print_info("Starting API tests...")
    print_info(f"Target: {BASE_URL}")
    print_info("Make sure your API is running before continuing!")

    input(f"\n{Colors.YELLOW}Press Enter to start tests...{Colors.END}")

    tester = APITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
