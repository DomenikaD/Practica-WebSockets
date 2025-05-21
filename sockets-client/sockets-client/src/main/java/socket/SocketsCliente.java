package socket;

import controlador.ClienteControlador;
import java.util.concurrent.atomic.AtomicInteger;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;
import vista.ClienteVista;


public class SocketsCliente {

    private static final AtomicInteger clientCounter = new AtomicInteger(1);

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JButton openClientBtn = new JButton("➕ Nuevo Cliente");

            openClientBtn.addActionListener(e -> {
                String clientName = "Cliente " + clientCounter.getAndIncrement();
                ClienteVista view = new ClienteVista();
                new ClienteControlador(view, clientName);
                view.setVisible(true);
            });

            JFrame launcherFrame = new JFrame("Clientes");
            launcherFrame.setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);
            launcherFrame.setSize(250, 100);
            launcherFrame.setLocationRelativeTo(null);
            launcherFrame.add(openClientBtn);
            launcherFrame.setVisible(true);
        });
}
}
