#ifndef PFILTER_H
#define PFILTER_H

#include <vector>
#include <functional>
#include <algorithm>
#include <iterator>
#include <iostream>
#include <random>

#include "statefun.h"
#include "obsvfun.h"
#include "proposal.h"
#include "sampler.h"
#include "resampler.h"
#include "binder3rd.h"
#include "compose3.h"

/// this is the particle filter template
/// To use it, the user should define the state type and observation type
/// where the operator '+', '<<' and '>>' of state type should be predefined.
/// To construct an object, the user should give four function pointers as listed below.
/// The user can also use four function objects to initialize the pfilter object.
/// In that case, automatic type conversion will be called.


template<class state_type, class obsv_type>
class ParticleFilter
{
    public:
        ParticleFilter(precision_type (*fptr)(state_type,state_type),
                precision_type (*gptr)(state_type, obsv_type),
                precision_type (*qptr)(state_type, state_type, obsv_type),
                state_type (*q_sam_ptr)(state_type, obsv_type)); ///< declaration of constructor

        virtual ~ParticleFilter();

        state_type update(obsv_type y);
        void initialize(int pn); ///< initialize with the number of particles we want to use

    protected:
        /// hide these functions
        ParticleFilter();
        ParticleFilter( const ParticleFilter& other);
        ParticleFilter& operator=(const ParticleFilter& other);

        state_type mX; ///< estimated data
        std::vector<state_type> mXI1; ///< particles
        std::vector<state_type> mXI2; ///< particles
        std::vector<precision_type> mWI; ///< weights of particles

        statefun<state_type> mF; ///< pdf for state move
        obsvfun<state_type, obsv_type> mG; ///< pdf for observation function
        proposal<state_type,obsv_type> mQ; ///< pdf of the proposal distribution
        sampler<state_type,obsv_type> mQSampler; ///< sampler of the proposal distribution
        resampler<state_type> mResampler; ///< resampler

        int mParticleNum; ///< number of particles

};


/*template<class state_type, class obsv_type>
pfilter<state_type, obsv_type>::pfilter()
{
    //ctor
}*/


template<class state_type, class obsv_type>
ParticleFilter<state_type, obsv_type>::ParticleFilter (precision_type (*fptr)(state_type, state_type),
                                         precision_type (*gptr)(state_type, obsv_type),
                                         precision_type (*qptr)(state_type, state_type, obsv_type),
                                         state_type (*q_sam_ptr)(state_type, obsv_type)):
    mF(fptr),
    mG(gptr),
    mQ(qptr),
    mQSampler(q_sam_ptr),
    mResampler(mWI,mXI2,mXI1),
    mParticleNum(0)
{


}


template<class state_type, class obsv_type>
ParticleFilter<state_type, obsv_type>::~ParticleFilter()
{
    //dtor
}

/*template<class state_type, class obsv_type>
pfilter<state_type, obsv_type>::pfilter(const pfilter& other)
{
    //copy ctor
}*/

/*template<class state_type, class obsv_type>
pfilter<state_type, obsv_type>& pfilter<state_type, obsv_type>::
operator=(const pfilter& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}*/

template<class state_type, class obsv_type>
state_type ParticleFilter<state_type, obsv_type>::update(obsv_type y)
{
    transform ( mXI1.begin(), mXI1.end(), mXI2.begin(), std::bind2nd(mQSampler, y) );
    transform ( mXI2.begin(), mXI2.end(),
                mXI1.begin(), mWI.begin(),
               bind3rd(compose3<state_type,obsv_type>(mF,mG,mQ),y) );
    mResampler();
    mX = accumulate(mXI1.begin(), mXI1.end(), 0.0)/mParticleNum;

    return mX;
}

template<class state_type, class obsv_type>
void ParticleFilter<state_type, obsv_type>::initialize(int pn){
        mParticleNum = pn;
        mXI1.resize(mParticleNum,0);
        mXI2.resize(mParticleNum,0);
        mWI.resize(mParticleNum,0);
}

#endif // PFILTER_H
