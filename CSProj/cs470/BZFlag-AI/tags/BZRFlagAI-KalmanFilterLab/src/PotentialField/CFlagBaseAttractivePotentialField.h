/*
 * CBaseAttractivePotentialField.h
 *
 *  Created on: Sep 29, 2012
 *      Author: walter
 */

#ifndef CFLAGBASEATTRACTIVEPOTENTIALFIELD_H_
#define CFLAGBASEATTRACTIVEPOTENTIALFIELD_H_

#include "../Base/CBase.h"
#include "../Base/CFlag.h"
#include "CAttractivePotentialField.h"

class CFlagBaseAttractivePotentialField: public CAttractivePotentialField {
public:
	CFlagBaseAttractivePotentialField(CFlag* flag, CBase * base);
	virtual ~CFlagBaseAttractivePotentialField();

	CBase * getBase(void) { return mpBase; };
	CFlag * getFlag(void) { return mpFlag; };
private:
	void init();
	CBase * mpBase;
	CFlag * mpFlag;
};

#endif /* CBASEATTRACTIVEPOTENTIALFIELD_H_ */
