// ======================================================================
// \title  FlagSvrComponentImpl.cpp
// \author has
// \brief  cpp file for FlagSvr component implementation class
//
// \copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================


#include <QualsRef/FlagSvr/FlagSvrComponentImpl.hpp>
#include "Fw/Types/BasicTypes.hpp"
#include <Fw/Logger/Logger.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <string>
#include <vector>

#define LOG_MSG_SIZE 128

static uint32_t validCountRequired = FLAG_VALID_COUNT;

namespace Ref {

  bool isValid(int n);
  // ----------------------------------------------------------------------
  // Construction, initialization, and destruction
  // ----------------------------------------------------------------------

  // const std::string FlagSvrComponentImpl::m_theFlagCode = FLAG_CODE;

  FlagSvrComponentImpl ::
    FlagSvrComponentImpl(
        const char *const compName
    ) : FlagSvrComponentBase(compName)
  {

  }

  void FlagSvrComponentImpl ::
    init(
        const NATIVE_INT_TYPE instance
    )
  {
    FlagSvrComponentBase::init(instance);
    Fw::Logger::logMsg("Init FlagSvr\n");
    this->m_FlagSvrNoopCnt = 0;
    this->m_theFlag.resize(160);
    std::ifstream flagDataFile(FLAG_DATA_FILE);
    if(flagDataFile.is_open()) {
      std::ostringstream ss;
      ss << flagDataFile.rdbuf();
      this->m_theFlag = ss.str();
      flagDataFile.close();
      remove(FLAG_DATA_FILE);
      Fw::Logger::logMsg("FLAG: %s\n", reinterpret_cast<POINTER_CAST>(this->m_theFlag.c_str()));
    } else {
      Fw::Logger::logMsg("Could not open flag data file on startup");
    }
  }

  FlagSvrComponentImpl ::
    ~FlagSvrComponentImpl(void)
  {

  }

  // ----------------------------------------------------------------------
  // Command handler implementations
  // ----------------------------------------------------------------------
  // Credit https://en.wikipedia.org/wiki/Primality_test
  bool isValid(int n) {
    if (n == 2 || n ==3 )
      return true;
    
    if (n <= 1 || n % 2 == 0 || n % 3 == 0)
        return false;

    for (int i = 5; i * i <= n; i += 6)
    {
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    }
  }

  int convertStringToNum(std::string input, int* output) {
    char *end;
    int retVal = -1;
    errno = 0;

    const char* buff = input.c_str();
  
    const long uval = strtol(input.c_str(), &end, 10);
  
    if (end == buff) {
      fprintf(stderr, "%s: not a decimal number\n", buff);
    } else if ('\0' != *end) {
      fprintf(stderr, "%s: extra characters at end of input: %s\n", buff, end);
    } else if ((LONG_MIN == uval || LONG_MAX == uval) && ERANGE == errno) {
      fprintf(stderr, "%s out of range of type long\n", buff);
    } else if (uval > INT_MAX) {
      fprintf(stderr, "%ld greater than INT_MAX\n", uval);
    } else if (uval < INT_MIN) {
      fprintf(stderr, "%ld less than INT_MIN\n", uval);
    } else {
      *output = (int)uval;
      retVal = 0;
    }
    return retVal;
  }

  void FlagSvrComponentImpl :: FS_FlagEnable_cmdHandler(
    const FwOpcodeType opCode,
    const U32 cmdSeq,
    const Fw::CmdStringArg& inputFile
  )
  {   
    char msg[LOG_MSG_SIZE];
    bool unlocked = false;
    std::string flagAttemptStr;
    int num;
    int status;
    unsigned invalid = 0;
    size_t ccount = 0;
    std::vector<int> numbers;
    size_t pos = 0;
    std::string delim = ",";

    std::string inputFileName = inputFile.toChar();

    if (inputFileName.size() == 0) {
      inputFileName = FLAG_ATTEMPT_FILE_DEFAULT;
    }

    snprintf(msg, LOG_MSG_SIZE, "Loading %s file for flag enable attempt", inputFileName.c_str());
    Fw::LogStringArg logStr(msg);
    this->log_ACTIVITY_HI_FS_FLAG_DATA_ATTEMPT(logStr);
  
    std::ifstream flagAttemptFile(inputFileName.c_str());
    std::vector<std::string> attemptVector;
    if(flagAttemptFile.is_open()) {
      std::string line;
      while(std::getline(flagAttemptFile, line)) {
        attemptVector.push_back(line);
      }
      flagAttemptFile.close();
    } else {
      logStr = Fw::LogStringArg("Error opening flag attempt file");
      this->log_ACTIVITY_HI_FS_LOG_EVENT(logStr);
    }
    
    // while (pos = flagAttemptStr.find(delim) != std::string::npos) {
    //   numberStringVector.push_back(flagAttemptStr.substr(0,pos));
    //   flagAttemptStr.erase(0, pos + delim.length());
    // }

    for (unsigned i=0; i<attemptVector.size(); i++) {
      std::string item = attemptVector[i];
      status = convertStringToNum(item, &num);
      if (status == 0) {
        if(isValid(num)) {
          numbers.push_back(num);
        } else {
          invalid++;
        }
      }
    }

    snprintf(msg, LOG_MSG_SIZE, "Items Parsed: %lu, Valid Items: %lu, Invalid Items: %u", attemptVector.size(), numbers.size(), invalid);
    logStr = Fw::LogStringArg(msg);
    this->log_ACTIVITY_HI_FS_FLAG_DATA_ATTEMPT(logStr);

    if (numbers.size() == validCountRequired && invalid == 0) {
      unlocked = true;
      logStr == Fw::LogStringArg("--- Flag Unlocked ---");
      this->log_ACTIVITY_HI_FS_FLAG_DATA_ATTEMPT(logStr);
    } else {
      if(numbers.size() != validCountRequired || invalid > 0){
        logStr = Fw::LogStringArg("--- Flag Not Unlocked, Fix Input and Try Again ---");
      }
      this->log_ACTIVITY_HI_FS_FLAG_DATA_ATTEMPT(logStr);
    }

    if(unlocked) {
      snprintf(msg, LOG_MSG_SIZE, "Flag Unlocked Successfull with %lu of %u valid items",  numbers.size(), validCountRequired);
      logStr = Fw::LogStringArg(msg);
      this->log_ACTIVITY_HI_FS_FLAG_DATA_ATTEMPT(logStr);
      Fw::Logger::logMsg("Flag Unlocked. Flag: %s\n", reinterpret_cast<POINTER_CAST>(this->m_theFlag.c_str()));

      std::ofstream out("flag.txt");
      out << this->m_theFlag;
      out.close();

      logStr = Fw::LogStringArg("flag.txt");
      this->log_ACTIVITY_HI_FS_FLAG_DATA(logStr);
      this->cmdResponse_out(opCode,cmdSeq,Fw::COMMAND_OK);
 
    }
  }

  void FlagSvrComponentImpl ::
    FS_FlagSvrNoop_cmdHandler(
        const FwOpcodeType opCode,
        const U32 cmdSeq
    )
  {
    this->m_FlagSvrNoopCnt++;
    this->tlmWrite_FS_NOOP_CNT(this->m_FlagSvrNoopCnt);
    this->cmdResponse_out(opCode,cmdSeq,Fw::COMMAND_OK);
  }

} // end namespace Ref
