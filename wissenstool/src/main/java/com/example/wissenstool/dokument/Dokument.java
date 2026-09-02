package com.example.wissenstool.dokument;
import jakarta.persistence.*;

public class Dokument {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String titel;

    private String name;

    @Lob

    private String content;

    protected Dokument(String titel, String content) {
        this.content = content;
        this.name = titel;
    }

    public long getId() {
        return id;
    }

    public String getTitel() {
        return titel;
    }

    public String getContent() {
        return content;
    }

    public void setTitel(String titel) {
        this.titel = titel;
    }

    public void setContent(String content) {
        this.content = content;
    }
    
}
        
