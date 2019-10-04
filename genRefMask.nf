#!/usr/bin/env nextflow
/* 
Mask a reference (fasta file) using script bin/genRefMask.py
nextflow run genRefMask.nf --refFile /data/references/compass/fasta/NC_000962_3.fasta --outputPath mask_75_90
*/


// parameters 
params.outputPath = "example_output"
params.refFile = "example_data/R00000039.fasta"

// initial logging
log.info "\n" 
log.info "BUGflow -- version 0.1"
log.info "Input reference file   :  ${params.refFile}"
log.info "Output path            :  ${params.outputPath}"
log.info "Container engine       :  ${workflow.containerEngine}"
log.info "Container              :  ${workflow.container}"
log.info "Profile                :  ${workflow.profile}"
log.info "\n"


// rename input parameters
refFasta = file(params.refFile)
outputPath = file(params.outputPath)

// Build indexes for reference fasta file - bwa, samtools, repeatmask
process indexReference {
  
    input:
        file refFasta
	
	output:
		file "*" into ref_index
	
	tag {refFasta}
	publishDir "$outputPath/reference/${refFasta.baseName}", mode: 'copy'

    """
    #bwa index
    bwa index $refFasta
    
    #samtools index
    samtools faidx $refFasta
    
    #blast indexes for self-self blast
	makeblastdb -dbtype nucl -in $refFasta
    
    #reference mask
    genRefMask.py -r $refFasta -m 75 -p 90
    bgzip -c ${refFasta}.rpt.regions > ${refFasta.baseName}.rpt_mask.gz
	echo '##INFO=<ID=RPT,Number=1,Type=Integer,Description="Flag for variant in repetitive region">' > ${refFasta.baseName}.rpt_mask.hdr
	tabix -s1 -b2 -e3 ${refFasta.baseName}.rpt_mask.gz
    genRefArray.py -g ${refFasta}.rpt.regions -r $refFasta > ${refFasta.baseName}_repmask.array
    """
}

