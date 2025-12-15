from src.metrics import (
    calcular_taxa_detecao,
    calcular_falsos_positivos,
    medir_latencia,
    calcular_throughput
)
import time


def test_taxa_detecao():
    eventos = [
        {"detectado": True, "era_ataque": True},   # VP
        {"detectado": False, "era_ataque": True},  # FN
        {"detectado": True, "era_ataque": False},  # FP
    ]

    taxa = calcular_taxa_detecao(eventos)
    assert taxa == 1/2  # 1 ataque detectado / 2 ataques reais


def test_falsos_positivos():
    eventos = [
        {"detectado": True, "era_ataque": False},  # FP
        {"detectado": False, "era_ataque": False}, # TN
        {"detectado": True, "era_ataque": True},   # VP
    ]

    fp = calcular_falsos_positivos(eventos)
    assert fp == 1/2  # 1 FP / 2 eventos normais


def test_latencia():
    def funcao_teste():
        time.sleep(0.01)

    lat = medir_latencia(funcao_teste)
    assert lat >= 0.01


def test_throughput():
    thr = calcular_throughput(100, 2)
    assert thr == 50  # 50 eventos por segundo
