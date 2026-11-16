
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const EnergiaInteligenteApp());
}

class EnergiaInteligenteApp extends StatelessWidget {
  const EnergiaInteligenteApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Energia-Inteligente',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.green,
        ),
        useMaterial3: true,
      ),
      home: const TelaSimulacao(),
    );
  }
}

class TelaSimulacao extends StatefulWidget {
  const TelaSimulacao({super.key});

  @override
  State<TelaSimulacao> createState() => _TelaSimulacaoState();
}

class _TelaSimulacaoState extends State<TelaSimulacao> {
  final _formKey = GlobalKey<FormState>();

  final _consumoController = TextEditingController();
  final _localizacaoController = TextEditingController();
  final _areaController = TextEditingController();
  final _investimentoController = TextEditingController();

  @override
  void dispose() {
    _consumoController.dispose();
    _localizacaoController.dispose();
    _areaController.dispose();
    _investimentoController.dispose();
    super.dispose();
  }

  Widget campoTexto({
    required String titulo,
    required String dica,
    required IconData icone,
    required TextEditingController controller,
    TextInputType teclado = TextInputType.text,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextFormField(
        controller: controller,
        keyboardType: teclado,
        decoration: InputDecoration(
          labelText: titulo,
          hintText: dica,
          prefixIcon: Icon(icone),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        validator: (valor) {
          if (valor == null || valor.trim().isEmpty) {
            return 'Preencha este campo';
          }

          if (teclado != TextInputType.text) {
            final numero = double.tryParse(
              valor.trim().replaceAll(',', '.'),
            );

            if (numero == null || !numero.isFinite || numero <= 0) {
              return 'Informe um número maior que zero';
            }
          }

          return null;
        },
      ),
    );
  }

  Future<void> simular() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    final dados = {
      'consumoMensal': double.parse(
        _consumoController.text.trim().replaceAll(',', '.'),
      ),
      'localizacao': _localizacaoController.text.trim(),
      'areaDisponivel': double.parse(
        _areaController.text.trim().replaceAll(',', '.'),
      ),
      'investimento': double.parse(
        _investimentoController.text.trim().replaceAll(',', '.'),
      ),
    };

    try {
      final resposta = await http.post(
        Uri.parse('http://localhost:8080/api/simulacoes'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(dados),
      );

      if (!mounted) return;

      if (resposta.statusCode == 200 || resposta.statusCode == 201) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Simulação salva com sucesso!'),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erro ao salvar: ${resposta.statusCode}'),
          ),
        );
      }
    } catch (erro) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro de conexão com a API: $erro'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Energia-Inteligente'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(
                Icons.solar_power,
                size: 64,
                color: Colors.green,
              ),
              const SizedBox(height: 12),
              const Text(
                'Simule sua energia limpa',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Informe os dados para avaliar alternativas '
                    'de energia para sua residência ou empresa.',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 28),
              campoTexto(
                titulo: 'Consumo mensal (kWh)',
                dica: 'Ex.: 350',
                icone: Icons.bolt,
                controller: _consumoController,
                teclado: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
              ),
              campoTexto(
                titulo: 'Localização',
                dica: 'Cidade ou CEP',
                icone: Icons.location_on,
                controller: _localizacaoController,
              ),
              campoTexto(
                titulo: 'Área disponível (m²)',
                dica: 'Ex.: 40',
                icone: Icons.roofing,
                controller: _areaController,
                teclado: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
              ),
              campoTexto(
                titulo: 'Investimento disponível (R\$)',
                dica: 'Ex.: 10000',
                icone: Icons.account_balance_wallet,
                controller: _investimentoController,
                teclado: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
              ),
              const SizedBox(height: 8),
              FilledButton.icon(
                onPressed: simular,
                icon: const Icon(Icons.eco),
                label: const Text('Simular energia'),
                style: FilledButton.styleFrom(
                  backgroundColor: Colors.green,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(
                    vertical: 16,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'ODS 7 — Energia Limpa e Acessível',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.green,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
