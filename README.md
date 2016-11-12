# polygon2domjudge
A simple program to convert CodeForces Polygon ZIP packages to Domjudge ZIP Packages

    usage: p2d.py [-h] [--code CODE] [--sample SAMPLE] [--color COLOR] [-o OUTPUT]
                  [--no-delete]
                  package
    
    Process Polygon Package to Domjudge Package.
    
    positional arguments:
      package               path of the polygon package
    
    optional arguments:
      -h, --help            show this help message and exit
      --code CODE           problem code for domjudge
      --sample SAMPLE       Specify the filename for sample test. Defaults to '01'
      --color COLOR         problem color for domjudge (in #XXXXXX format)
      -o OUTPUT, --output OUTPUT
                            Output Package directory
      --no-delete           Don't delete the output directory
