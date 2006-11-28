# Makefile for source rpm: libpcap
# $Id$
NAME := libpcap
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
