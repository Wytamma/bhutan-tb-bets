BETS_DIR = OUT_DIR / "BETS"

rule BETS:
    input:
        alignment=config["alignment"],
        template=TEMPLATES_DIR / "{template}.xml"
    output:
        tracelog = BETS_DIR / "{template}/logs/{template}.log",
        posteriorlog = BETS_DIR / "{template}/logs/{template}.posterior.log",
        screenlog = BETS_DIR / "{template}/{template}.out", # ML estiamtes are printed to screen
        # treelog = BETS_DIR / "{template}/logs/{template}.trees",
    params:
        particle_count = config["BETS"].get("particle_count"),
        subchain_length = config["BETS"].get("subchain_length"),
        constant_site_weights = config["beast"].get("constant_site_weights"),
    conda:
        "../envs/beast.yml"
    threads: config["BETS"].get("threads")
    resources:
        **config["BETS"].get("resources", {}),
    envmodules:
        *config["BETS"].get("envmodules", []),
    shell:
        """
        pybeast \
            --run bash \
            --gpu \
            --chain-length 100000 \
            --group {BETS_DIR} \
            --duplicates 1 \
            --ns \
            -d "alignment={input.alignment}" \
            -d "constantSiteWeights={params.constant_site_weights}" \
            -d "mcmc.particleCount={params.particle_count}" \
            -d "mcmc.subChainLength={params.subchain_length}" \
            --overwrite \
            {input.template}
        """

rule process_bets:
    input:
        expand(
            BETS_DIR / "{template}/{template}.out",
            template=config["BETS"].get("templates")
        ),
    output:
         BETS_DIR / "BETS.png"
    conda:
        "../envs/python.yml"
    localrule: True
    shell:
        """
        python {SCRIPT_DIR}/process_BETS.py {BETS_DIR}
        """