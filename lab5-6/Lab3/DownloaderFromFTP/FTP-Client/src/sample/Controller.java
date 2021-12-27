package sample;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.paint.Color;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;
import org.apache.commons.net.ftp.FTPClient;

import java.io.File;
import java.io.FileOutputStream;

public class Controller {
    @FXML
    public Button DirectoryChooserButton;
    @FXML
    public Button DownloadButton;
    @FXML
    public Label ResultMessage;
    @FXML
    public TextField PathTpFileText;
    @FXML
    public TextField DirectoryText;

    private String currentDirectory;

    @FXML
    public void DirectoryChooserButtonClick()
    {
        try {
            DirectoryChooser directoryChooser = new DirectoryChooser();
            directoryChooser.setInitialDirectory(new File("E:\\"));
            directoryChooser.setTitle("Choose directory for file");
            File file = directoryChooser.showDialog(new Stage());
            if (file != null) {
                currentDirectory = file.toString();
                DirectoryText.setText(currentDirectory);
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    @FXML
    public void DownloadButtonClick() {
        File file = null;
        boolean result = false;
        try {
            FTPClient fClient = new FTPClient();
            String path =  PathTpFileText.getText();
            String[] temp = path.split("/");
            String fileName = temp[temp.length -1];
            file = new File(currentDirectory, fileName);
            file.createNewFile();
            FileOutputStream fileOutputStream = new FileOutputStream(file);

            try {
                fClient.connect("test.rebex.net");
                fClient.enterLocalPassiveMode();
                fClient.login("demo", "password");
                if (fClient.retrieveFile(path, fileOutputStream))
                {
                    result = true;
                }
                fClient.logout();
                fileOutputStream.close();
                fClient.disconnect();

            } catch (Exception ex) {
                result = false;
                System.err.println(ex);
            }
        } catch (Exception e) {
            result = false;
            System.out.println(e.getMessage());
        }
        if (result)
        {
            ResultMessage.setTextFill(Color.GREEN);
            ResultMessage.setText("Successfully downloaded");
        }
        else
        {
            ResultMessage.setTextFill(Color.RED);
            ResultMessage.setText("Download failed");
            if (file != null)
            {
                file.delete();
            }
        }
    }
}
