// Copyright 2018-2020 Polyaxon, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/*
 * Polyaxon SDKs and REST API specification.
 * Polyaxon SDKs and REST API specification.
 *
 * The version of the OpenAPI document: 1.0.82
 * Contact: contact@polyaxon.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


package org.openapitools.client.model;

import java.util.Objects;
import java.util.Arrays;
import com.google.gson.TypeAdapter;
import com.google.gson.annotations.JsonAdapter;
import com.google.gson.annotations.SerializedName;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import java.io.IOException;

/**
 * V1IoCond
 */
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2020-04-24T20:53:44.256+02:00[Europe/Berlin]")
public class V1IoCond {
  public static final String SERIALIZED_NAME_KIND = "kind";
  @SerializedName(SERIALIZED_NAME_KIND)
  private String kind = "io";

  public static final String SERIALIZED_NAME_PARAM = "param";
  @SerializedName(SERIALIZED_NAME_PARAM)
  private String param;

  public static final String SERIALIZED_NAME_TRIGGER = "trigger";
  @SerializedName(SERIALIZED_NAME_TRIGGER)
  private String trigger;


  public V1IoCond kind(String kind) {
    
    this.kind = kind;
    return this;
  }

   /**
   * Get kind
   * @return kind
  **/
  @javax.annotation.Nullable
  @ApiModelProperty(value = "")

  public String getKind() {
    return kind;
  }


  public void setKind(String kind) {
    this.kind = kind;
  }


  public V1IoCond param(String param) {
    
    this.param = param;
    return this;
  }

   /**
   * Get param
   * @return param
  **/
  @javax.annotation.Nullable
  @ApiModelProperty(value = "")

  public String getParam() {
    return param;
  }


  public void setParam(String param) {
    this.param = param;
  }


  public V1IoCond trigger(String trigger) {
    
    this.trigger = trigger;
    return this;
  }

   /**
   * Get trigger
   * @return trigger
  **/
  @javax.annotation.Nullable
  @ApiModelProperty(value = "")

  public String getTrigger() {
    return trigger;
  }


  public void setTrigger(String trigger) {
    this.trigger = trigger;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    V1IoCond v1IoCond = (V1IoCond) o;
    return Objects.equals(this.kind, v1IoCond.kind) &&
        Objects.equals(this.param, v1IoCond.param) &&
        Objects.equals(this.trigger, v1IoCond.trigger);
  }

  @Override
  public int hashCode() {
    return Objects.hash(kind, param, trigger);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class V1IoCond {\n");
    sb.append("    kind: ").append(toIndentedString(kind)).append("\n");
    sb.append("    param: ").append(toIndentedString(param)).append("\n");
    sb.append("    trigger: ").append(toIndentedString(trigger)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(java.lang.Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }

}
