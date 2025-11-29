import time

def calcular_taxa_detecao(eventos):
    """
    eventos = lista de dicionários, ex:
    {"detectado": True/False, "era_ataque": True/False}
    """
    total_ataques = sum(1 for e in eventos if e["era_ataque"])
    if total_ataques == 0:
        return 0
    
    verdadeiros_positivos = sum(1 for e in eventos if e["detectado"] and e["era_ataque"])
    return verdadeiros_positivos / total_ataques


def calcular_falsos_positivos(eventos):
    total_normais = sum(1 for e in eventos if not e["era_ataque"])
    if total_normais == 0:
        return 0

    falsos_positivos = sum(1 for e in eventos if e["detectado"] and not e["era_ataque"])
    return falsos_positivos / total_normais


def medir_latencia(funcao, *args, **kwargs):
    """
    Mede o tempo (latência) de execução de uma função.
    """
    inicio = time.time()
    funcao(*args, **kwargs)
    fim = time.time()
    return fim - inicio


def calcular_throughput(total_eventos, tempo_total):
    if tempo_total == 0:
        return 0
    return total_eventos / tempo_total
