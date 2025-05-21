/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package controlador;

import model.ClienteSocket;
import vista.ClienteVista;

/**
 *
 * @author Domenika Delgado
 */
public class ClienteControlador {
    private final ClienteSocket model;
    private final ClienteVista view;

    public ClienteControlador(ClienteVista view, String username) {
        this.view = view;
        this.model = new ClienteSocket();

        view.setClientName(username);

        try {
            // Intentamos conectar al servidor (puerto y host puedes ajustar)
            model.setUsername(username);
            model.connect("localhost", 5000, message -> view.appendMessage(message));
            view.appendMessage("Conectado como " + username);
        } catch (Exception ex) {
            view.appendMessage("Error al conectar: " + ex.getMessage());
            return;
        }

        // Agregamos listener al botón de enviar
        view.addSendButtonListener(e -> {
            String msg = view.getMessageInput();
            if (!msg.isEmpty()) {
                model.sendMessage(msg);
                view.clearMessageInput();
            }
        });
        
         view.addWindowListener(new java.awt.event.WindowAdapter() {
            @Override
            public void windowClosing(java.awt.event.WindowEvent e) {
                model.disconnect();
            }
        });
    }

    public void close() {
        model.disconnect();
        view.close();
    }
    
   
}
