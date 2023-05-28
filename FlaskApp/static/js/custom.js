// console.log("Sanity check!");
// var stripe = Stripe('pk_live_51MoHqnBRa4aUdrbV2nGLnO1z4n7HK1ot5luCmEgDLynG1AToxO2nnifroox4QlEYnmvR1uRIcUeQeFOgTx6aWck700neNZR82b');

// var checkoutButton = document.querySelector('#checkout-button');
// checkoutButton.addEventListener('click', function () {
//   stripe.redirectToCheckout({
//     lineItems: [{
//       // Define the product and price in the Dashboard first, and use the price
//       // ID in your client-side code. You may also pass a SKU id into the `price`
//       // field
//       price: 'price_1NCCOEBRa4aUdrbVOadSUFVz',
//       quantity: 1
//     }],
//     mode: 'subscription',
//     successUrl: 'http://localhost:5000/success',
//     cancelUrl: 'http://localhost:5000/cancel'
//   });
// });
