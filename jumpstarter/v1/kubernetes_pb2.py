# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: jumpstarter/v1/kubernetes.proto
# Protobuf Python Version: 5.28.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    0,
    '',
    'jumpstarter/v1/kubernetes.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fjumpstarter/v1/kubernetes.proto\x12\x0ejumpstarter.v1\"`\n\x18LabelSelectorRequirement\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x1a\n\x08operator\x18\x02 \x01(\tR\x08operator\x12\x16\n\x06values\x18\x03 \x03(\tR\x06values\"\xf9\x01\n\rLabelSelector\x12U\n\x11match_expressions\x18\x01 \x03(\x0b\x32(.jumpstarter.v1.LabelSelectorRequirementR\x10matchExpressions\x12Q\n\x0cmatch_labels\x18\x02 \x03(\x0b\x32..jumpstarter.v1.LabelSelector.MatchLabelsEntryR\x0bmatchLabels\x1a>\n\x10MatchLabelsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42~\n\x12\x63om.jumpstarter.v1B\x0fKubernetesProtoP\x01\xa2\x02\x03JXX\xaa\x02\x0eJumpstarter.V1\xca\x02\x0eJumpstarter\\V1\xe2\x02\x1aJumpstarter\\V1\\GPBMetadata\xea\x02\x0fJumpstarter::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'jumpstarter.v1.kubernetes_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\022com.jumpstarter.v1B\017KubernetesProtoP\001\242\002\003JXX\252\002\016Jumpstarter.V1\312\002\016Jumpstarter\\V1\342\002\032Jumpstarter\\V1\\GPBMetadata\352\002\017Jumpstarter::V1'
  _globals['_LABELSELECTOR_MATCHLABELSENTRY']._loaded_options = None
  _globals['_LABELSELECTOR_MATCHLABELSENTRY']._serialized_options = b'8\001'
  _globals['_LABELSELECTORREQUIREMENT']._serialized_start=51
  _globals['_LABELSELECTORREQUIREMENT']._serialized_end=147
  _globals['_LABELSELECTOR']._serialized_start=150
  _globals['_LABELSELECTOR']._serialized_end=399
  _globals['_LABELSELECTOR_MATCHLABELSENTRY']._serialized_start=337
  _globals['_LABELSELECTOR_MATCHLABELSENTRY']._serialized_end=399
# @@protoc_insertion_point(module_scope)
