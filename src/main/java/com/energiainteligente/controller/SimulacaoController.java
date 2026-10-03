package com.energiainteligente.controller;

import com.energiainteligente.model.Simulacao;
import com.energiainteligente.repository.SimulacaoRepository;
import com.energiainteligente.service.InteligenciaArtificialService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/simulacoes")
public class SimulacaoController {

    private final SimulacaoRepository repository;
    private final InteligenciaArtificialService iaService;

    public SimulacaoController(
            SimulacaoRepository repository,
            InteligenciaArtificialService iaService) {

        this.repository = repository;
        this.iaService = iaService;
    }

    @PostMapping
    public Simulacao salvar(@RequestBody Simulacao simulacao) {
        return repository.save(simulacao);
    }

    @GetMapping
    public Iterable<Simulacao> listar() {
        return repository.findAll();
    }

    @PostMapping("/{id}/analise")
    public String analisar(@PathVariable Long id) {

        Simulacao simulacao = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Simulação não encontrada"));

        String analise = iaService.analisar(simulacao);

        simulacao.setAnaliseIa(analise);
        repository.save(simulacao);

        return analise;
    }
}