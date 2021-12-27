package sample;

import javafx.fxml.FXML;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class Controller {
    @FXML
    private TextField WebAddressText;
    @FXML
    private TextArea SourceCode;

    @FXML
    private void getSourceCodeButtonClick() {
        SourceCode.setText("");
        try {
            URL url = new URL(WebAddressText.getText());
            try {
                URLConnection urlConnection = url.openConnection();
                BufferedReader reader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                String string = reader.readLine();
                while (string != null) {
                    SourceCode.setText(SourceCode.getText() + "\n" + string);
                    string = reader.readLine();
                }
            } catch (Exception e) {
                SourceCode.setText("Something failed");
                System.out.println(e.getMessage());
            }
        } catch (Exception e) {
            SourceCode.setText("Bad URL");
            System.out.println(e.getMessage());
        }
    }
}
