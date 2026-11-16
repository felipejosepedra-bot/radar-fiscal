#!/usr/bin/env python3
"""Incorpora alterações verificadas, preservando histórico e evitando duplicações."""
import argparse
import json
import os
from pathlib import Path
from datetime import date
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parents[1] / "atualizacoes.json"
RADARES = {"Reforma Tributária", "Fiscal Estadual", "Isenções de Medicamentos", "LE Logística", "Relatório Farmacêutico"}
FIELDS = ["id", "titulo", "resumo", "publicacao", "norma", "antes", "depois", "providencias"]
def rows_from(v):
    if isinstance(v, list): return v
    if isinstance(v, dict) and isinstance(v.get("atualizacoes"), list): return v["atualizacoes"]
    if isinstance(v, dict) and "id" in v: return [v]
    raise ValueError('Esperado registro JSON ou {"atualizacoes":[...]}.')
def verify(v):
    if not isinstance(v,dict): raise ValueError("Registro não é objeto.")
    for k in FIELDS:
        if not isinstance(v.get(k),str) or not v[k].strip(): raise ValueError("Campo obrigatório: "+k)
    for k in ("publicacao", "vigencia"):
        if v.get(k):
            if date.fromisoformat(v[k]).isoformat()!=v[k]: raise ValueError("Data inválida "+k)
    for k in ("uf","tema","impacto"):
        if not isinstance(v.get(k),list) or not v[k]: raise ValueError("Lista obrigatória: "+k)
    if not isinstance(v.get("fontes"),list) or not v["fontes"]: raise ValueError("Fonte oficial obrigatória.")
    for source in v["fontes"]:
        host=urlparse(source.get("url","")).hostname or ""
        if not source.get("titulo") or not any(host==x or host.endswith("."+x) for x in ("gov.br","leg.br","jus.br")):
            raise ValueError("URL de fonte não oficial ou título faltando.")
        if not source["url"].startswith("https://"):raise ValueError("Fonte exige HTTPS.")
    rs=v.get("radares",v.get("radar",["Reforma Tributária"]))
    if isinstance(rs,str):rs=[rs]
    if not isinstance(rs,list) or not rs or any(x not in RADARES for x in rs):raise ValueError("Radar de origem inválido.")
    v["radares"]=sorted(set(rs))
    v.pop("radar",None)
    return v
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--env",default="NOVOS_REGISTROS")
    p.add_argument("--github-output")
    args=p.parse_args()
    raw=os.environ.get(args.env,"")
    changed=False
    if raw.strip():
        incoming=[verify(x) for x in rows_from(json.loads(raw))]
        existing=json.loads(BASE.read_text(encoding="utf-8"))
        by_id={r["id"]:r for r in existing["atualizacoes"]}
        for item in incoming:
            old=by_id.get(item["id"])
            if old:
                # Preserva os radares que já encontraram este mesmo registro.
                item["radares"]=sorted(set(old.get("radares",["Reforma Tributária"])) | set(item["radares"]))
            if old!=item:
                by_id[item["id"]]=item
                changed=True
        if changed:
            output={"atualizacoes":sorted(by_id.values(),key=lambda x:(x.get("publicacao",""),x["id"]),reverse=True)}
            BASE.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if args.github_output:
        with open(args.github_output,"a",encoding="utf-8") as f:f.write("changed="+str(changed).lower()+"\n")
    print("Base modificada." if changed else "Sem registros novos; nenhuma alteração.")
if __name__=="__main__": main()
