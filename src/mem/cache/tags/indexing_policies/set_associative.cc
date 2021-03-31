/*
 * Copyright (c) 2018 Inria
 * Copyright (c) 2012-2014,2017 ARM Limited
 * All rights reserved.
 *
 * The license below extends only to copyright in the software and shall
 * not be construed as granting a license to any other intellectual
 * property including but not limited to intellectual property relating
 * to a hardware implementation of the functionality of the software
 * licensed hereunder.  You may use the software subject to the license
 * terms below provided that you ensure that this notice is replicated
 * unmodified and in its entirety in all distributions of the software,
 * modified or unmodified, in source code or in binary form.
 *
 * Copyright (c) 2003-2005,2014 The Regents of The University of Michigan
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Authors: Daniel Carvalho
 *          Erik Hallnor
 */

/**
 * @file
 * Definitions of a set associative indexing policy.
 */

#include "mem/cache/tags/indexing_policies/set_associative.hh"

#include "mem/cache/replacement_policies/replaceable_entry.hh"

#include "base/intmath.hh"
#include "debug/Cache.hh"


SetAssociative::SetAssociative(const Params *p)
    : BaseIndexingPolicy(p)
    {

    numSecurityDomains = p->numSecurityDomains;
    /*setMask = numSets/numSecurityDomains - 1;

    DPRINTF(Cache, "NumSets: %d, size %d, entry_size %d, assoc %d", numSets, p->size, p->entry_size, assoc);

    assert(numSecurityDomains != 0);
    assert(numSets/numSecurityDomains != 0);
    tagShift = setShift + floorLog2(numSets/numSecurityDomains);
    
    if (numSecurityDomains < 1 || !isPowerOf2(numSecurityDomains)){
        fatal("Number of security domains must be at least 1 and a power of 2");
    }

    if (numSets < numSecurityDomains) {
        fatal("Number of security domains must exceed number of sets!");
    }*/

}

uint32_t
SetAssociative::extractSet(const Addr addr, uint32_t securityDomain)
{
    /*
    int securityIndex;
    auto it = std::find(domainMapping.begin(), domainMapping.end(), securityDomain);
    if (it != domainMapping.end()) {
        securityIndex = it - domainMapping.begin();
    } else {
        securityIndex = domainMapping.size();
        DPRINTF(Cache, "New Security Index! Domain %x, Index %x", securityDomain, securityIndex);

        domainMapping.push_back(securityDomain);
    }

    assert(securityIndex < numSecurityDomains);
    assert(numSets/numSecurityDomains != 0);
    return ((addr >> setShift) & setMask) | (securityIndex << (floorLog2(numSets/numSecurityDomains)));
    */
    return (addr >> setShift) & setMask;
}

Addr
SetAssociative::regenerateAddr(const Addr tag, const ReplaceableEntry* entry)
                                                                        const
{
    //return (tag << tagShift) | ((entry->getSet() & setMask) << setShift);
    return (tag << tagShift) | (entry->getSet() << setShift);
}

std::vector<ReplaceableEntry*>
SetAssociative::getPossibleEntries(const Addr addr, uint32_t securityDomain)
{
    return sets[extractSet(addr, securityDomain)];
}

SetAssociative*
SetAssociativeParams::create()
{
    return new SetAssociative(this);
}
