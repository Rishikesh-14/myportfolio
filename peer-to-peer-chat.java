import java.io.*;
import java.net.*;
import java.util.Scanner;

public class PeerToPeerChat {
    private static final int PORT = 12345;
    private static String partnerIP = "";
    private static boolean isRunning = true;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== Peer-to-Peer Chat ===");
        System.out.print("Enter partner IP (leave empty if initiating connection): ");
        partnerIP = scanner.nextLine();

        // Start listening thread
        new Thread(PeerToPeerChat::listenForMessages).start();

        // Start sending thread
        new Thread(() -> {
            try (DatagramSocket socket = new DatagramSocket()) {
                InetAddress partnerAddress = partnerIP.isEmpty() ? null : InetAddress.getByName(partnerIP);
                
                System.out.println("Type messages (enter 'exit' to quit):");
                while (isRunning) {
                    String message = scanner.nextLine();
                    if ("exit".equalsIgnoreCase(message)) {
                        isRunning = false;
                        break;
                    }
                    
                    if (partnerAddress != null) {
                        byte[] buffer = message.getBytes();
                        DatagramPacket packet = new DatagramPacket(
                            buffer, buffer.length, partnerAddress, PORT);
                        socket.send(packet);
                    }
                }
            } catch (IOException e) {
                System.err.println("Error sending: " + e.getMessage());
            }
        }).start();
    }

    private static void listenForMessages() {
        try (DatagramSocket socket = new DatagramSocket(PORT)) {
            byte[] buffer = new byte[1024];
            
            while (isRunning) {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                socket.receive(packet);
                
                // If we didn't set a partner initially, use whoever messaged us first
                if (partnerIP.isEmpty()) {
                    partnerIP = packet.getAddress().getHostAddress();
                    System.out.println("\nConnected to: " + partnerIP);
                }
                
                String received = new String(packet.getData(), 0, packet.getLength());
                System.out.println("\nReceived: " + received);
                System.out.print("> ");
            }
        } catch (IOException e) {
            if (isRunning) { // Only show error if we didn't intentionally stop
                System.err.println("Error receiving: " + e.getMessage());
            }
        }
    }
}