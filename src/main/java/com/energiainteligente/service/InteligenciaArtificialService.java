package com.energiainteligente.service;

import com.energiainteligente.model.Simulacao;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.List;
import java.util.Map;

@Service
public class InteligenciaArtificialService {

    private final RestClient restClient;

    public InteligenciaArtificialService() {
        this.restClient = RestClient.create(
                "https://integrate.api.nvidia.com"
        );
    }

    public String prepararPrompt(Simulacao simulacao) {

        return "Analise brevemente esta simulação de energia residencial. "
                + "Responda em português, em no máximo 5 linhas, informando "
                + "se o investimento parece viável e uma justificativa simples. "
                + "Consumo mensal: " + simulacao.getConsumoMensal() + " kWh"
                + ", Área disponível: " + simulacao.getAreaDisponivel() + " m²"
                + ", Investimento: R$ " + simulacao.getInvestimento()
                + ", Localização: " + simulacao.getLocalizacao();
    }

    public String analisar(Simulacao simulacao) {

        String apiKey = System.getenv("NVIDIA_API_KEY");

        if (apiKey == null || apiKey.isBlank()) {
            throw new RuntimeException("NVIDIA_API_KEY não configurada.");
        }

        String prompt = prepararPrompt(simulacao);

        Map<String, Object> requisicao = Map.of(
                "model", "nvidia/nemotron-3-super-120b-a12b",
                "messages", List.of(
                        Map.of(
                                "role", "user",
                                "content", prompt
                        )
                ),
                "max_tokens", 1500,
                "temperature", 0.3
        );

        Map resposta = restClient.post()
                .uri("/v1/chat/completions")
                .header("Authorization", "Bearer " + apiKey)
                .body(requisicao)
                .retrieve()
                .body(Map.class);

        List<Map<String, Object>> choices =
                (List<Map<String, Object>>) resposta.get("choices");

        Map<String, Object> message =
                (Map<String, Object>) choices.get(0).get("message");

        return (String) message.get("content");
    }
}