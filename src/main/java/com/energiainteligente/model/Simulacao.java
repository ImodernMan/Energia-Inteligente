package com.energiainteligente.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.PositiveOrZero;

@Entity
public class Simulacao {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @PositiveOrZero(message = "Consumo mensal não pode ser negativo")
    private double consumoMensal;

    @PositiveOrZero(message = "Área disponível não pode ser negativa")
    private double areaDisponivel;

    @PositiveOrZero(message = "Investimento não pode ser negativo")
    private double investimento;

    @NotBlank(message = "Localização é obrigatória")
    private String localizacao;

    // Resposta gerada pela Inteligência Artificial
    private String analiseIa;

    public Simulacao() {
    }

    public Simulacao(
            Long id,
            double consumoMensal,
            double areaDisponivel,
            double investimento,
            String localizacao) {
        this.id = id;
        this.consumoMensal = consumoMensal;
        this.areaDisponivel = areaDisponivel;
        this.investimento = investimento;
        this.localizacao = localizacao;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public double getConsumoMensal() {
        return consumoMensal;
    }

    public void setConsumoMensal(double consumoMensal) {
        this.consumoMensal = consumoMensal;
    }

    public double getAreaDisponivel() {
        return areaDisponivel;
    }

    public void setAreaDisponivel(double areaDisponivel) {
        this.areaDisponivel = areaDisponivel;
    }

    public double getInvestimento() {
        return investimento;
    }

    public void setInvestimento(double investimento) {
        this.investimento = investimento;
    }

    public String getLocalizacao() {
        return localizacao;
    }

    public void setLocalizacao(String localizacao) {
        this.localizacao = localizacao;
    }

    public String getAnaliseIa() {
        return analiseIa;
    }

    public void setAnaliseIa(String analiseIa) {
        this.analiseIa = analiseIa;
    }
}
