package org.example;

import com.google.gson.Gson;
import org.example.domain.Order;
import org.junit.Test;

public class OrderTest {

    @Test
    public void testJson() {
        Order order = new Order();
        order.setSku("sky");
        order.setQuantity(2);
        order.setCustomerId("cust001");
        Gson gson = new Gson();
        System.out.println(gson.toJson(order));
    }
}
