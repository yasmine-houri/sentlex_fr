try:
    import sentlex.sentanalysis as sentdoc
except Exception:
    import sentanalysis as sentdoc

try:
    import sentlex.sentlex as sentlex
except Exception:
    import sentlex as sentlex

import sys,os
import unittest

#####
#
# Unit Testing for doc sentiment analysis
#
####

#
# Data
#
TESTDOC_ADJ = 'good/JJ good/JJ good/JJ' 
TESTDOC_NOTAG = 'this cookie is good. it is very good indeed'
TESTDOC_BADADJ = 'bad_JJ Bad_JJ bAd_JJ'
TESTDOC_NEGATED = 'not/DT bad/JJ ./. not/DT really/RR bad/JJ'

# T0 - Basic Class functionality
class T0_parameter_setting(unittest.TestCase):
    def runTest(self):
        # empty list
        ds = sentdoc.BasicDocSentiScore()
        ds.verbose=True

        ds.set_neg_detection(True, 15)
        ds.set_active_pos(True, False, False, False)

        self.assertEqual((ds.a, ds.v, ds.n, ds.r), (True, False, False, False), 'Failed set POS parameters')
        self.assertEqual((ds.negation, ds.negation_window), (True, 15), 'Failed set negation')

        ds.set_parameters(score_mode=ds.SCOREONCE, score_freq=True, negation=False)
        print ds.score_mode, ds.score_freq, ds.negation
        self.assertEqual(ds.score_mode, ds.SCOREONCE, 'Unable to set parameters via kwards')
        self.assertEqual(ds.score_freq, True, 'Unable to set parameters via kwards')
        self.assertEqual(ds.negation, False, 'Unable to set parameters via kwards')


class T1_scoring_documents(unittest.TestCase):
    def runTest(self):
        # load lexicon
        L = sentlex.MobyLexicon()
        self.assertTrue(L.is_loaded, 'Test lexicon did not load correctly')

        # create a class that scores only adjectives
        ds = sentdoc.BasicDocSentiScore()
        ds.verbose=True
        ds.set_active_pos(True, False, False, False)
        ds.set_parameters(score_mode=ds.SCOREALL, score_freq=False, negation=False)
        ds.set_lexicon(L)

        # separator ok?
        self.assertEqual(ds._detect_tag(TESTDOC_ADJ), '/', 'Unable to detect correct separator')

        # now score!
        (dpos, dneg) = ds.classify_document(TESTDOC_ADJ, verbose=True)
        self.assertTrue(ds.resultdata and ds.resultdata.has_key('doc') and ds.resultdata.has_key('annotated_doc')\
            and ds.resultdata.has_key('resultpos') and ds.resultdata.has_key('resultneg'), 'Did not populate resultdata after scoring doc')

        self.assertTrue(dpos > dneg, 'Did not find positive words on positive doc')
        print 'TESTDOC_ADJ (pos,neg): %2.2f %2.2f' % (dpos, dneg)

        # again, for negative text
        (dpos, dneg) = ds.classify_document(TESTDOC_BADADJ, verbose=True)
        self.assertTrue(dneg > dpos, 'Did not find negative words on negative doc')
        print 'TESTDOC_BADADJ (pos,neg): %2.2f %2.2f' % (dpos, dneg)

        # negated text
        ds.set_neg_detection(True, 5)
        (dpos, dneg) = ds.classify_document(TESTDOC_NEGATED, verbose=True)
        self.assertTrue(dpos > dneg, 'Did not find positive words on TESTDOC_NEGATED')
        print 'TESTDOC_NEGATED (pos,neg): %2.2f %2.2f' % (dpos, dneg)

#
# Runs unit testing if module is called directly
#
if __name__ == "__main__":
    
   # Run those guys
   unittest.main()