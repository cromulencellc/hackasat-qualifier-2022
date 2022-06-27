// ======================================================================
// \title  FlagSvrComponentImpl.hpp
// \author has
// \brief  hpp file for FlagSvr component implementation class
//
// \copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================

#ifndef FlagSvr_HPP
#define FlagSvr_HPP

#include "QualsRef/FlagSvr/FlagSvrComponentAc.hpp"
#include <string>

#define FLAG_DATA_FILE ".FlagData"
#define FLAG_ATTEMPT_FILE_DEFAULT "attempt.txt"
#define FLAG_VALID_COUNT 2022

namespace Ref {


  class FlagSvrComponentImpl :
    public FlagSvrComponentBase
  {

    public:

      // ----------------------------------------------------------------------
      // Construction, initialization, and destruction
      // ----------------------------------------------------------------------

      //! Construct object FlagSvr
      //!
      FlagSvrComponentImpl(
          const char *const compName /*!< The component name*/
      );

      //! Initialize object FlagSvr
      //!
      void init(
          const NATIVE_INT_TYPE instance = 0 /*!< The instance number*/
      );

      //! Destroy object FlagSvr
      //!
      ~FlagSvrComponentImpl(void);

    PRIVATE:

      // ----------------------------------------------------------------------
      // Command handler implementations
      // ----------------------------------------------------------------------

      //! Implementation for FS_FlagEnable command handler
      //! Command to enable flag
      void FS_FlagEnable_cmdHandler(
          const FwOpcodeType opCode, /*!< The opcode*/
          const U32 cmdSeq, /*!< The command sequence number*/
          const Fw::CmdStringArg& inputFile /*!< 
                    Input File for flag attempt
                    */
      );

      //! Implementation for FS_FlagSvrNoop command handler
      //! FlagSvr NOOP Command
      void FS_FlagSvrNoop_cmdHandler(
          const FwOpcodeType opCode, /*!< The opcode*/
          const U32 cmdSeq /*!< The command sequence number*/
      );

      // Noop Counter Private
      U32 m_FlagSvrNoopCnt;
      std::string m_theFlag;

    };

    

} // end namespace Ref

#endif
