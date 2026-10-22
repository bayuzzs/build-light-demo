import unittest

from calculator import CartItem, OrderSummary, checkout


class CheckoutTest(unittest.TestCase):
    def test_multiple_items_and_quantities(self):
        cart = [CartItem("Keyboard", 80_000), CartItem("Cable", 20_000, 2)]
        self.assertEqual(checkout(cart), OrderSummary(120_000, 0, 0, 120_000))

    def test_voucher_reduces_total(self):
        cart = [CartItem("Keyboard", 80_000), CartItem("Desk mat", 40_000)]
        self.assertEqual(checkout(cart, "HEMAT10"), OrderSummary(120_000, 12_000, 0, 108_000))

    def test_shipping_threshold_uses_discounted_subtotal(self):
        cart = [CartItem("Headset", 100_000)]
        self.assertEqual(checkout(cart, "HEMAT20"), OrderSummary(100_000, 20_000, 15_000, 95_000))

    def test_voucher_normalization_and_rounding(self):
        self.assertEqual(checkout([CartItem("Cable", 15_999)], " hemat10 ").discount, 1_599)

    def test_rejects_invalid_cart_and_voucher(self):
        with self.assertRaises(ValueError):
            checkout([])
        with self.assertRaises(ValueError):
            checkout([CartItem("Cable", 20_000)], "UNKNOWN")
        for args in [("", 100, 1), ("Cable", -1, 1), ("Cable", 100, 0), ("Cable", 1.5, 1)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                CartItem(*args)


if __name__ == "__main__":
    unittest.main()
