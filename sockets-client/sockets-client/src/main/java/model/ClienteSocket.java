/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package model;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.function.Consumer;

/**
 *
 * @author Domenika Delgado
 */
public class ClienteSocket {
    private Socket socket;
    private BufferedReader in;
    private PrintWriter out;
    private Thread listenerThread;
    private String username = "Anon";

    public void setUsername(String name) {
        this.username = name;
    }

    public void connect(String server, int port, Consumer<String> onMessageReceived) throws IOException {
        socket = new Socket(server, port);
        in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        out = new PrintWriter(socket.getOutputStream(), true);

        // Hilo para escuchar mensajes del servidor
        listenerThread = new Thread(() -> {
            try {
                String msg;
                while ((msg = in.readLine()) != null) {
                    onMessageReceived.accept(msg);
                }
            } catch (IOException e) {
                onMessageReceived.accept("⚠️ Conexión cerrada o error.");
            }
        });
        listenerThread.setDaemon(true);
        listenerThread.start();
    }

    public void sendMessage(String message) {
        if (out != null) {
            out.println("[" + username + "]: " + message);
        }
    }

    public void disconnect() {
        try {
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
            if (listenerThread != null && listenerThread.isAlive()) {
                listenerThread.interrupt();
            }
        } catch (IOException e) {
            // Silencioso o log
        }
    }
}

