import numpy as np

class XVA():
    """
    Simple class to derive an implied PD
    from a CDS Spread and vice-versa and to
    calculate a CVA(or DVA) adjustment
    recovery_rate: Suggestion over ~40%
    t: Time to Maturity in years
    spread: CDS Spread of your counterparty in bps (3% = 300bps)
    """

    def __init__(self,t,recovery_rate,spread):
        self.t = t
        self.recovery_rate = recovery_rate
        self.spread = spread/10000

    def prob_default(self):
        pdefault = 1 - np.exp((-self.spread * self.t)/ (1-self.recovery_rate))
        return pdefault

    def cds_spread(self,p_default):
        cds = np.log(1-p_default) * ((self.recovery_rate-1)/self.t)
        return cds

    def calculate(self,npv):
        '''
        NPV shall be the total NPV of your derivatives portfolio.
        '''
        if npv > 0: #CVA
            adjustment = npv * self.prob_default() * (1 - self.recovery_rate)
            print('{:>12,.2f}'.format(adjustment))
        else: #DVA
            adjustment = npv * self.prob_default() * (1 - self.recovery_rate)
            print('{:>12,.2f}'.format(adjustment))
        return adjustment

if __name__ == "__main__":
    product_details = XVA(2,0.40,300) #2y Swap ; Counterparty CDS Spread:300bps
    value_adjustment = product_details.calculate(1e6) #Notional: 1,000,000 NPV
