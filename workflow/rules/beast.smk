BEAST_DIR = OUT_DIR / "beast"

rule beast:
    input:
        alignment = config["alignment"],
        template = TEMPLATES_DIR / "{template}.xml"
    output:
        tracelog = BEAST_DIR / "{template}/logs/{template}.log",
        treelog = BEAST_DIR / "{template}/logs/{template}.trees",
    conda:
        "../envs/beast.yml"
    params:
        chain_length = config["beast"].get("chain_length"),
        constant_site_weights = config["beast"].get("constant_site_weights"),
    threads: config["beast"].get("threads")
    resources:
        **config["beast"].get("resources", {}),
    envmodules:
        *config["beast"].get("envmodules", []),
    shell:
        """
        pybeast \
            --run bash \
            --gpu \
            --chain-length {params.chain_length} \
            --samples 10000 \
            --group "{BEAST_DIR}" \
            -d "alignment={input.alignment}" \
            -d "constantSiteWeights={params.constant_site_weights}" \
            -d "tracelog={wildcards.template}.log" \
            -d "treelog={wildcards.template}.trees" \
            --overwrite \
            {input.template}
        """