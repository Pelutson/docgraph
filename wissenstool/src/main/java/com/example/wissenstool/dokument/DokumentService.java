package  com.example.wissenstool.dokument;


import java.util.List;

import org.springframework.stereotype.Service;


@Service

public class DokumentService {
    private final DokumentRepository dokumentRepository;

    public DokumentService(DokumentRepository dokumentRepository) {
        this.dokumentRepository = dokumentRepository;
    }

    public List<Dokument> getAllDokumente() {
        return dokumentRepository.findAll();
    }

    public Dokument getDokumentById(Long id) {
        return dokumentRepository.findById(id).orElse(null);
    }

    public Dokument saveDokument(Dokument dokument) {
        return dokumentRepository.save(dokument);
    }

    public void deleteDokument(Long id) {
        dokumentRepository.deleteById(id);
    }
}
