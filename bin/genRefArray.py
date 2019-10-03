import sys
import argparse

def load_reference(reflines):
    reference = [x.strip() for x in reflines if x and x[0] not in ['>']]
    reference = ''.join(reference)
    return reference

def load_regions(regionlines):
    regions = [x.split('\t')[1:-1] for x in regionlines if x and x[0] not in ['>', '#']]
    regions = [(int(x[0]), int(x[1])) for x in regions]
    return regions

def generate_array(regions, reflen):
    mask = list('0' * reflen)

    for low, high in regions:
        for x in range(low, high + 1):
            mask[x - 1] = '1'

    mask = ''.join(mask)
    return mask

def intersperse(data, linelen, sep='\n'):
    ret = list()
    lines = (len(data) // linelen) + 1
    for x in range(0, lines-1):
        ret.append(data[x*linelen:(x+1)*linelen] + sep)
    ret.append(data[(lines - 1)*linelen:])
    return ''.join(ret)

def main():
    '''
    Generate mask array file based on repetitive region (bed file), in the following format:
    # number from 1, coordinates inclusive of start and stop
    NC_000962.3 5   10	1
    NC_000962.3	80184	80373	1

    Input:
        -r reference file
        -g region bed file
    
    Output:
        masked array file (0 for nomask, 1 for mask)

    Run:
        python3 bin/genRefArray.py -g NC_000962_3.fasta.rpt.regions -r ref.fa
    '''
    parser = argparse.ArgumentParser(description='Generate mask array')

    parser.add_argument('-r', '--reference', dest='reference', help='path to the reference file')
    parser.add_argument('-g', '--regions', dest='regions', help='masked region from blast')

    args = parser.parse_args()

    regionlines = open(args.regions).readlines()
    regions = load_regions(regionlines)
       
    reflines = open(args.reference).readlines()
    reference = load_reference(reflines)

    mask = generate_array(regions, len(reference))

    intersperse(mask, 100, '\n')


if __name__ == "__main__":
    main()