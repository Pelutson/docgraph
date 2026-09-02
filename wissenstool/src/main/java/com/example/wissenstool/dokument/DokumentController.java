package com.example.wissenstool.dokument;
import org.apache.catalina.Service;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;





@RestController
@RequestMapping("/api/dokumente")
public class DokumentController {
    private final DokumentService dokumentService;
    public DokumentController(DokumentService dokumentService) {
        this.dokumentService = dokumentService;
    }
    @GetMapping
    public List<Dokument> getAllDokumente() {
        return dokumentService.getAllDokumente();
    }
    @GetMapping("/id")
    public Dokument einzeln(@PathVariable Long id) {
        return dokumentService.getDokumentById(id);
    }

    @PostMapping("/{id}")
    public String postMethodName(@RequestBody DokumentDto dto) {
        return dokumentService.saveDokument(dto.titel(), dto.content());
    }

    @DeleteMapping("/{id}")
    public void deleteDokument(@PathVariable Long id) {
        dokumentService.deleteDokument(id);
    }
    
    


    

}
