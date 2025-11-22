const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

let orders = [];

app.post('/api/orders', (req, res) => {
    const order = {
        id: orders.length + 1,
        ...req.body,
        status: 'pending',
        createdAt: new Date().toISOString()
    };
    orders.push(order);
    res.json({ success: true, orderId: order.id });
});

app.listen(3000, () => {
    console.log('Backend server running on port 3000');
});