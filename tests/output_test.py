import unittest, re
import business.queries.sitelink_queries as query
import business.services.quickstatements_service as qs_svc
import business.utils.url_utils as url_utils
import domain.localizations as loc
from business.services.quickstatements_service import QuickStatementsService 
from business.quickstatement import QuickStatement
import business.utils.quickstatememnts_utils as qs_utils 
from business.mapping import LinkMapping

class OutputTest(unittest.TestCase):
    def test_generate_db_reference_on_each_domain(self):
        # Arrange
        qs_svc = QuickStatementsService()
        items = {
            # Unknown
            # '' : QuickStatement(link="archive.org"), #"https://archive.org/details/$1"
            # '' : QuickStatement(link="https://collection.britishmuseum.org/resource/?uri=http%3A%2F%2Fcollection.britishmuseum.org%2Fid%2Fperson-institution%2F52959"), #null
            # '' : QuickStatement(link="https://en.wikisource.org/wiki/Zerffi,_George_Gustavus_(DNB00)"), #null
            
            # Refreshed
            # '' : QuickStatement(link="www.bbc.co.uk"), #"https://artuk.org/discover/artworks/search/actor:$1"

            # Non found in dump?
            # '' : QuickStatement(link="rkd.nl"), #"https://rkd.nl/en/explore/artists/$1"
            # '' : QuickStatement(link="www.uni-stuttgart.de"), #"http://www.uni-stuttgart.de/hi/gnt/dsi2/index.php?table_name=dsi&function=details&where_field=id&where_value=$1"

            # Known
            '"18040949"' : QuickStatement(link="https://collection.cooperhewitt.org/people/18040949/bio"), #"https://collection.cooperhewitt.org/people/$1/"
            '"irvine-kenneth-john-ken-12682"' : QuickStatement(link="http://adb.anu.edu.au/biography/irvine-kenneth-john-ken-12682"), #"http://adb.anu.edu.au/biography/$1"
            '"weight-carel-victor-morlais-19081997"' : QuickStatement(link="https://artuk.org/discover/artists/weight-carel-victor-morlais-19081997"), #"https://artuk.org/discover/artists/$1"
            '"cahnw"' : QuickStatement(link="https://dictionaryofarthistorians.org/cahnw.html"), #"https://dictionaryofarthistorians.org/$1.html"
            '"Graeff,_op_den_(Opdegraf,_Updegrave,_Updegrove)_family"' : QuickStatement(link="http://gameo.org/index.php?title=Graeff,_op_den_(Opdegraf,_Updegrave,_Updegrove)_family"), #"http://gameo.org/index.php?title=$1"
            '"495"' : QuickStatement(link="http://munksroll.rcplondon.ac.uk/Biography/Details/495"), #"http://munksroll.rcplondon.ac.uk/Biography/Details/$1"
            '"msib2_1217424563"' : QuickStatement(link="http://sculpture.gla.ac.uk/view/person.php?id=msib2_1217424563"), #"http://sculpture.gla.ac.uk/view/person.php?id=$1"
            '"500355683"' : QuickStatement(link="http://vocab.getty.edu/ulan/500355683"), #"http://vocab.getty.edu/page/ulan/$1"
            '"geoffrey-ricardo/"' : QuickStatement(link="https://www.daao.org.au/bio/geoffrey-ricardo/"), #"https://www.daao.org.au/bio/$1"
            '"I00029938"' : QuickStatement(link="http://www.genealogics.org/getperson.php?personID=I00029938&tree=LEO"), #"http://www.genealogics.org/getperson.php?personID=$1&tree=LEO"
            '"140"' : QuickStatement(link="http://www.museothyssen.org/en/thyssen/ficha_artista/140"), #"http://www.museothyssen.org/en/thyssen/ficha_artista/$1"
            '"1885"' : QuickStatement(link="http://www.newulsterbiography.co.uk/index.php/home/viewPerson/1885"), #"http://www.newulsterbiography.co.uk/index.php/home/viewPerson/$1"
            '"321/000094039"' : QuickStatement(link="http://www.nndb.com/people/321/000094039/"), #"http://www.nndb.com/people/$1/"
            '"aved"' : QuickStatement(link="https://www.wga.hu/bio/a/aved/biograph.html"), #"http://www.wga.hu/bio/a/$1/biograph.html"
            '"bos"' : QuickStatement(link="https://www.wga.hu/bio/b/bos/biograph.html"), #"http://www.wga.hu/bio/b/$1/biograph.html"
            '"copley"' : QuickStatement(link="https://www.wga.hu/bio/c/copley/biograph.html"), #"http://www.wga.hu/bio/c/$1/biograph.html"
            '"dodin"' : QuickStatement(link="https://www.wga.hu/bio/d/dodin/biograph.html"), #"http://www.wga.hu/bio/d/$1/biograph.html"
            '"espinosb"' : QuickStatement(link="https://www.wga.hu/bio/e/espinosb/biograph.html"), #"http://www.wga.hu/bio/e/$1/biograph.html"
            '"filloeul"' : QuickStatement(link="https://www.wga.hu/bio/f/filloeul/biograph.html"), #"http://www.wga.hu/bio/f/$1/biograph.html"
            '"guglie"' : QuickStatement(link="https://www.wga.hu/bio/g/guglie/biograph.html"), #"http://www.wga.hu/bio/g/$1/biograph.html"
            '"hackert/philipp"' : QuickStatement(link="https://www.wga.hu/bio/h/hackert/philipp/biograph.html"), #"http://www.wga.hu/bio/h/$1/biograph.html"
            '"ives"' : QuickStatement(link="https://www.wga.hu/bio/i/ives/biograph.html"), #"http://www.wga.hu/bio/i/$1/biograph.html"
            '"jacquet"' : QuickStatement(link="https://www.wga.hu/bio/j/jacquet/biograph.html"), #"http://www.wga.hu/bio/j/$1/biograph.html"
            '"kobell/jan2"' : QuickStatement(link="https://www.wga.hu/bio/k/kobell/jan2/biograph.html"), #"http://www.wga.hu/bio/k/$1/biograph.html"
            '"lieberma"' : QuickStatement(link="https://www.wga.hu/bio/l/lieberma/biograph.html"), #"http://www.wga.hu/bio/l/$1/biograph.html"
            '"marilhat"' : QuickStatement(link="https://www.wga.hu/bio/m/marilhat/biograph.html"), #"http://www.wga.hu/bio/m/$1/biograph.html"
            '"niccolo/arca"' : QuickStatement(link="https://www.wga.hu/bio/n/niccolo/arca/biograph.html"), #"http://www.wga.hu/bio/n/$1/biograph.html"
            '"orlovsky"' : QuickStatement(link="https://www.wga.hu/bio/o/orlovsky/biograph.html"), #"http://www.wga.hu/bio/o/$1/biograph.html"
            '"powers"' : QuickStatement(link="https://www.wga.hu/bio/p/powers/biograph.html"), #"http://www.wga.hu/bio/p/$1/biograph.html"
            '"quarengh"' : QuickStatement(link="https://www.wga.hu/bio/q/quarengh/biograph.html"), #"http://www.wga.hu/bio/q/$1/biograph.html"
            '"reinhold"' : QuickStatement(link="https://www.wga.hu/bio/r/reinhold/biograph.html"), #"http://www.wga.hu/bio/r/$1/biograph.html"
            '"stranove"' : QuickStatement(link="https://www.wga.hu/bio/s/stranove/biograph.html"), #"http://www.wga.hu/bio/s/$1/biograph.html"
            '"tiepolo/lorenzo"' : QuickStatement(link="https://www.wga.hu/bio/t/tiepolo/lorenzo/biograph.html"), #"http://www.wga.hu/bio/t/$1/biograph.html"
            '"ugolino/tedice"' : QuickStatement(link="https://www.wga.hu/bio/u/ugolino/tedice/biograph.html"), #"http://www.wga.hu/bio/u/$1/biograph.html"
            '"vanderly"' : QuickStatement(link="https://www.wga.hu/bio/v/vanderly/biograph.html"), #"http://www.wga.hu/bio/v/$1/biograph.html"
            '"wtewael/joachim"' : QuickStatement(link="https://www.wga.hu/bio/w/wtewael/joachim/biograph.html"), #"http://www.wga.hu/bio/w/$1/biograph.html"
            '"xavery"' : QuickStatement(link="https://www.wga.hu/bio/x/xavery/biograph.html"), #"http://www.wga.hu/bio/x/$1/biograph.html"
            '"yvon"' : QuickStatement(link="https://www.wga.hu/bio/y/yvon/biograph.html"), #"http://www.wga.hu/bio/y/$1/biograph.html"
            '"zaryanko"' : QuickStatement(link="https://www.wga.hu/bio/z/zaryanko/biograph.html"), #"http://www.wga.hu/bio/z/$1/biograph.html"
            '"s2-HOWE-HEN-1869.html"' : QuickStatement(link="http://yba.llgc.org.uk/en/s2-HOWE-HEN-1869.html"), #"http://yba.llgc.org.uk/en/$1"
        }
        # Act 
        for key, value in items.iteritems():
            reference = qs_svc.generate_db_reference(value)

            print("\nLoad: {0} \t Reference: {1}\n".format(value.sitelink, reference))
            # Assert 
            self.assertIn(key, reference)
            print("\t OK")