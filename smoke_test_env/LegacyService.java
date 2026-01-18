
package com.example;
import io.vertx.core.AbstractVerticle;
import io.vertx.core.Promise;

public class LegacyService extends AbstractVerticle {
    public void start(Promise<Void> startFuture) {
        System.out.println("Start");
        startFuture.complete();
    }
}
    