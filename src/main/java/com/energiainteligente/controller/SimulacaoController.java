package com.energiainteligente.controller;

import com.energiainteligente.model.Simulacao;
import com.energiainteligente.repository.SimulacaoRepository;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/simulacoes")
public class SimulacaoController {

    private final SimulacaoRepository repository;

    public SimulacaoController(SimulacaoRepository repository) {
        this.repository = repository;
    }

    @PostMapping
    public Simulacao salvar(@RequestBody Simulacao simulacao) {
        return repository.save(simulacao);
    }

    @GetMapping
    public Iterable<Simulacao> listar() {
        return repository.findAll();
    }
}