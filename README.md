# Delivery Order Price Calculator (DOPC)

## Installation and Setup Guide

### 1. **Prerequisites**
   Ensure that you have Python (recommended Python 3.8 or higher) installed on your system.

### 2. **Install Dependencies**
   Once you have Python set up, install all the required dependencies by running:

   ```
   pip install -r requirements.txt
   ```

### 3. **Run the Application**
   After installing the required libraries, you can run the application by executing the following command:

   ```
   python main.py
   ```

   The application will start running on `http://localhost:5000`.

### 4. **API Usage**
   The main endpoint of the API is `/api/v1/delivery-order-price`, which calculates the total delivery price based on the given parameters. You need to provide the following query parameters:
   
   - `venue_slug`: The unique identifier for the venue (e.g., `home-assignment-venue-helsinki`)
   - `cart_value`: The total value of the items in the shopping cart (in the smallest currency unit)
   - `user_lat`: The latitude of the user's location
   - `user_lon`: The longitude of the user's location

   Example of sending a request:

   ```
   curl "http://localhost:5000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
   ```

### 5. **Expected Response**
   The API will return a JSON response with the following structure:

   ```
   {
     "total_price": 1190,
     "small_order_surcharge": 0,
     "cart_value": 1000,
     "delivery": {
       "fee": 190,
       "distance": 177
     }
   }
   ```

   - `total_price`: The total price including the cart value, delivery fee, and any small order surcharge.
   - `small_order_surcharge`: The surcharge for small orders, which will be 0 if the cart value exceeds the minimum requirement.
   - `cart_value`: The value of the cart as provided in the request.
   - `delivery`: The delivery fee breakdown, including:
     - `fee`: The calculated delivery fee.
     - `distance`: The delivery distance in meters.

### 6. **Handling Errors**
   If the delivery is not possible (for example, if the distance is too long), the API will return an error response with a status code of 400:

   ```
   {
     "error": "Delivery is not possible due to distance being too far."
   }
   ```

### 7. **Testing**
   You can test the API by sending requests with different parameters to verify if the calculations are correct. Feel free to modify the input to test edge cases and error handling.

---

## Thank you for reviewing my submission!

